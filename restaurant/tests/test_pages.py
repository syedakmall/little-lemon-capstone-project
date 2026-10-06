from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from restaurant.models import Booking, Menu


class PageTest(TestCase):
    def test_public_pages_render(self):
        for name in ('home', 'about', 'menu-page', 'book'):
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_root_redirects_home(self):
        self.assertRedirects(self.client.get('/'), reverse('home'))

    def test_menu_lists_items(self):
        item = Menu.objects.create(title='Bruschetta', price='7.99', inventory=5)
        self.assertContains(self.client.get(reverse('menu-page')), 'Bruschetta')
        self.assertContains(self.client.get(reverse('menu-item-page', args=[item.pk])), '$7.99')

    def test_missing_menu_item_404(self):
        self.assertEqual(self.client.get(reverse('menu-item-page', args=[999])).status_code, 404)


class BookPageTest(TestCase):
    def test_valid_booking_saved(self):
        when = timezone.localtime() + timedelta(days=2)
        response = self.client.post(
            reverse('book'),
            {'name': 'Ana', 'number_of_guests': 3, 'booking_date': when.strftime('%Y-%m-%dT%H:%M')},
            follow=True,
        )
        self.assertContains(response, 'Thanks Ana')
        self.assertEqual(Booking.objects.count(), 1)

    def test_past_booking_rejected(self):
        when = timezone.localtime() - timedelta(days=1)
        response = self.client.post(
            reverse('book'),
            {'name': 'Ana', 'number_of_guests': 3, 'booking_date': when.strftime('%Y-%m-%dT%H:%M')},
        )
        self.assertContains(response, 'future date')
        self.assertFalse(Booking.objects.exists())


class ReservationsPageTest(TestCase):
    def test_staff_only(self):
        response = self.client.get(reverse('reservations'))
        self.assertEqual(response.status_code, 302)

    def test_shows_bookings_for_selected_day(self):
        staff = User.objects.create_user(username='staff', password='pass12345', is_staff=True)
        self.client.force_login(staff)
        when = timezone.localtime() + timedelta(days=3)
        Booking.objects.create(name='Ana', number_of_guests=2, booking_date=when)
        Booking.objects.create(name='Ben', number_of_guests=2, booking_date=when + timedelta(days=1))

        response = self.client.get(reverse('reservations'), {'date': when.date().isoformat()})
        self.assertContains(response, 'Ana')
        self.assertNotContains(response, 'Ben')
