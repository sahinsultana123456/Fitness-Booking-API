from django.contrib import admin
from .models import Instructor, FitnessClass, Booking

# Register your models here.
admin.site.register(Instructor)
admin.site.register(FitnessClass)
admin.site.register(Booking)
