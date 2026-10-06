from django import forms

from .models import Booking, validate_future


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'number_of_guests', 'booking_date']
        labels = {'booking_date': 'Date and time'}
        widgets = {
            'booking_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
        }

    def clean_booking_date(self):
        value = self.cleaned_data['booking_date']
        validate_future(value)
        return value
