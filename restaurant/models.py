from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

MAX_PARTY_SIZE = 12


def validate_future(value):
    if value < timezone.now():
        raise ValidationError('Bookings must be for a future date and time.')


class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    inventory = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['title']
        verbose_name = 'menu item'

    def __str__(self):
        return f'{self.title} : {self.price}'


class Booking(models.Model):
    name = models.CharField(max_length=255)
    number_of_guests = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(MAX_PARTY_SIZE)]
    )
    booking_date = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ['booking_date']

    def __str__(self):
        return f'{self.name} for {self.number_of_guests} on {self.booking_date:%Y-%m-%d %H:%M}'
