from rest_framework import serializers
from .models import Instructor, FitnessClass, Booking
from django.utils.timezone import localtime

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'email', 'bio', 'profile_picture']

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    date_time = serializers.SerializerMethodField()
    
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'date_time', 'instructor', 'difficulty', 'total_slots', 'available_slots']
    
    def get_date_time(self, obj):
        # Converts UTC datetime to local time (IST or whatever current timezone)
        return localtime(obj.date_time).strftime('%Y-%m-%d %H:%M:%S %Z')

class BookingSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booked_at']
