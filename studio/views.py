import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from django.db import transaction

logger = logging.getLogger(__name__)

@api_view(['GET'])
def list_upcoming_classes(request):
    logger.info("Fetching upcoming fitness classes")
    now = timezone.now()
    classes = FitnessClass.objects.filter(date_time__gte=now).order_by('date_time')
    serializer = FitnessClassSerializer(classes, many=True)
    logger.info(f"Returned {len(serializer.data)} upcoming classes")
    return Response(serializer.data)


@api_view(['POST'])
@transaction.atomic
def book_class(request):
    class_id = request.data.get('class_id')
    client_name = request.data.get('client_name')
    client_email = request.data.get('client_email')

    logger.info(f"Booking attempt for class_id={class_id} by {client_email}")

    if not all([class_id, client_name, client_email]):
        logger.warning("Booking failed due to missing required fields")
        return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        fitness_class = FitnessClass.objects.select_for_update().get(id=class_id)
    except FitnessClass.DoesNotExist:
        logger.error(f"Booking failed: Fitness class {class_id} not found")
        return Response({'error': 'Fitness class not found.'}, status=status.HTTP_404_NOT_FOUND)

    if fitness_class.is_full():
        logger.warning(f"Booking failed: No slots available for class {class_id}")
        return Response({'error': 'No slots available.'}, status=status.HTTP_400_BAD_REQUEST)

    if Booking.objects.filter(fitness_class=fitness_class, client_email=client_email).exists():
        logger.warning(f"Booking failed: Duplicate booking by {client_email} for class {class_id}")
        return Response({'error': 'You have already booked this class.'}, status=status.HTTP_400_BAD_REQUEST)

    booking = Booking.objects.create(
        fitness_class=fitness_class,
        client_name=client_name,
        client_email=client_email,
    )

    fitness_class.available_slots -= 1
    fitness_class.save()

    logger.info(f"Booking successful: {booking.id} for class {class_id} by {client_email}")
    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_bookings(request):
    client_email = request.GET.get('email')
    logger.info(f"Fetching bookings for email: {client_email}")

    if not client_email:
        logger.warning("Fetching bookings failed: Email query parameter missing")
        return Response({'error': 'Email query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(client_email=client_email).select_related('fitness_class').order_by('-booked_at')
    if not bookings.exists():
        logger.info(f"No bookings found for email: {client_email}")
        return Response({'message': 'No bookings found for this email.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookingSerializer(bookings, many=True)
    logger.info(f"Returned {len(serializer.data)} bookings for email: {client_email}")
    return Response(serializer.data)
