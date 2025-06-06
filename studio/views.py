from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from django.db import transaction


@api_view(['GET'])
def list_upcoming_classes(request):
    now = timezone.now()
    classes = FitnessClass.objects.filter(date_time__gte=now).order_by('date_time')
    serializer = FitnessClassSerializer(classes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@transaction.atomic
def book_class(request):
    class_id = request.data.get('class_id')
    client_name = request.data.get('client_name')
    client_email = request.data.get('client_email')

    if not all([class_id, client_name, client_email]):
        return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        fitness_class = FitnessClass.objects.select_for_update().get(id=class_id)
    except FitnessClass.DoesNotExist:
        return Response({'error': 'Fitness class not found.'}, status=status.HTTP_404_NOT_FOUND)

    if fitness_class.is_full():
        return Response({'error': 'No slots available.'}, status=status.HTTP_400_BAD_REQUEST)

    if Booking.objects.filter(fitness_class=fitness_class, client_email=client_email).exists():
        return Response({'error': 'You have already booked this class.'}, status=status.HTTP_400_BAD_REQUEST)

    booking = Booking.objects.create(
        fitness_class=fitness_class,
        client_name=client_name,
        client_email=client_email,
    )

    fitness_class.available_slots -= 1
    fitness_class.save()

    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_bookings(request):
    client_email = request.GET.get('email')
    if not client_email:
        return Response({'error': 'Email query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(client_email=client_email).select_related('fitness_class').order_by('-booked_at')
    if not bookings.exists():
        return Response({'message': 'No bookings found for this email.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
