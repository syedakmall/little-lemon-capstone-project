from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import Booking, Menu
from restaurant.serializers import BookingSerializer, MenuSerializer


class MenuApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='guest', password='pass12345')
        self.staff = User.objects.create_user(username='staff', password='pass12345', is_staff=True)
        self.pasta = Menu.objects.create(title='Pasta', price='18.99', inventory=7)
        Menu.objects.create(title='Bruschetta', price='7.99', inventory=5)

    def test_requires_authentication(self):
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MenuSerializer(Menu.objects.all(), many=True).data)

    def test_search(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('menu-list'), {'search': 'pas'})
        self.assertEqual([item['title'] for item in response.data], ['Pasta'])

    def test_retrieve(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('menu-detail', args=[self.pasta.pk]))
        self.assertEqual(response.data['title'], 'Pasta')

    def test_only_staff_can_write(self):
        payload = {'title': 'Soup', 'price': '5.00', 'inventory': 3}

        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post(reverse('menu-list'), payload).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            self.client.delete(reverse('menu-detail', args=[self.pasta.pk])).status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(self.staff)
        self.assertEqual(self.client.post(reverse('menu-list'), payload).status_code, status.HTTP_201_CREATED)


class BookingApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='guest', password='pass12345')
        self.client.force_authenticate(self.user)
        self.tomorrow = timezone.now() + timedelta(days=1)
        self.booking = Booking.objects.create(name='John', number_of_guests=2, booking_date=self.tomorrow)

    def test_requires_authentication(self):
        self.client.force_authenticate(None)
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BookingSerializer(Booking.objects.all(), many=True).data)

    def test_retrieve(self):
        response = self.client.get(reverse('booking-detail', args=[self.booking.pk]))
        self.assertEqual(response.data, BookingSerializer(self.booking).data)

    def test_create(self):
        payload = {'name': 'Jane', 'number_of_guests': 4, 'booking_date': self.tomorrow.isoformat()}
        response = self.client.post(reverse('booking-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_create_rejects_invalid_data(self):
        payload = {'name': '', 'number_of_guests': 0, 'booking_date': ''}
        response = self.client.post(reverse('booking-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data), {'name', 'number_of_guests', 'booking_date'})

    def test_create_rejects_past_date(self):
        payload = {'name': 'Jane', 'number_of_guests': 2, 'booking_date': (timezone.now() - timedelta(hours=1)).isoformat()}
        response = self.client.post(reverse('booking-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('booking_date', response.data)


class TokenAuthTest(APITestCase):
    def test_token_grants_access(self):
        User.objects.create_user(username='guest', password='pass12345')
        token = self.client.post(reverse('api-token-auth'), {'username': 'guest', 'password': 'pass12345'}).data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(self.client.get(reverse('menu-list')).status_code, status.HTTP_200_OK)
