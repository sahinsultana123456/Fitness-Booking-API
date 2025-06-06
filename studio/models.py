from django.db import models
from django.core.validators import MinValueValidator

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)

    def __str__(self):
        return self.name


class FitnessClass(models.Model):
    DIFFICULTY_LEVELS = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=100)
    date_time = models.DateTimeField(help_text="Scheduled time in IST")
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, related_name='classes')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='Beginner')
    total_slots = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_slots = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name} ({self.difficulty}) with {self.instructor} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

    def is_full(self):
        return self.available_slots <= 0


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('fitness_class', 'client_email')

    def __str__(self):
        return f"{self.client_name} booked {self.fitness_class.name} ({self.fitness_class.date_time.strftime('%Y-%m-%d %H:%M')})"