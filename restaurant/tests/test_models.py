from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from restaurant.models import Booking, Menu


class MenuModelTest(TestCase):
    def test_str(self):
        item = Menu.objects.create(title='Pasta', price=Decimal('18.99'), inventory=5)
        self.assertEqual(str(item), 'Pasta : 18.99')

    def test_ordered_by_title(self):
        Menu.objects.create(title='Pasta', price=1, inventory=1)
        Menu.objects.create(title='Bruschetta', price=1, inventory=1)
        self.assertEqual(list(Menu.objects.values_list('title', flat=True)), ['Bruschetta', 'Pasta'])

    def test_negative_price_rejected(self):
        item = Menu(title='Soup', price=Decimal('-1.00'), inventory=1)
        with self.assertRaises(ValidationError):
            item.full_clean()


class BookingModelTest(TestCase):
    def test_party_size_limits(self):
        when = timezone.now() + timedelta(days=1)
        for guests in (0, 13):
            with self.subTest(guests=guests), self.assertRaises(ValidationError):
                Booking(name='Sam', number_of_guests=guests, booking_date=when).full_clean()
