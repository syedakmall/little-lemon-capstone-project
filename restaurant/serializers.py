from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Booking, Menu, validate_future


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title', 'description', 'price', 'inventory']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'name', 'number_of_guests', 'booking_date']

    def validate_booking_date(self, value):
        try:
            validate_future(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        return value
