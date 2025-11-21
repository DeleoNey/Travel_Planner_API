from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta

from trips.models import Trip

User = get_user_model()


class TripCRUDTestCase(APITestCase):
    """Tests for CRUD operations for trips"""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testemail@gmail.com',
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            email = 'othertestemail@gmail.com',
        )

        self.trip = Trip.objects.create(
            user=self.user,
            title="Test Trip",
            description="Test description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            base_currency='USD'
        )

        self.client.force_authenticate(user=self.user)

    def test_get_trips_list(self):
        """Test: retrieving the list of trips"""
        url = '/api/trips/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check pagination
        if 'results' in response.data:
            self.assertGreaterEqual(len(response.data['results']), 1)
        else:
            self.assertGreaterEqual(len(response.data), 1)

    def test_create_trip(self):
        """Test: creating a new trip"""
        url = '/api/trips/'

        data = {
            'title': 'New Trip',
            'description': 'New trip description',
            'start_date': date.today() + timedelta(days=10),
            'end_date': date.today() + timedelta(days=20),
            'base_currency': 'EUR'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trip.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Trip')
        self.assertEqual(response.data['base_currency'], 'EUR')

    def test_get_trip_detail(self):
        """Test: retrieving trip details"""
        url = f'/api/trips/{self.trip.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Trip')
        self.assertEqual(response.data['base_currency'], 'USD')

    def test_update_trip(self):
        """Test: updating a trip"""
        url = f'/api/trips/{self.trip.id}/'

        data = {
            'title': 'Updated Trip',
            'description': 'Updated description',
            'start_date': self.trip.start_date,
            'end_date': self.trip.end_date,
            'base_currency': 'EUR'
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.title, 'Updated Trip')
        self.assertEqual(self.trip.base_currency, 'EUR')

    def test_partial_update_trip(self):
        """Test: partially updating a trip"""
        url = f'/api/trips/{self.trip.id}/'

        data = {
            'title': 'Partially Updated Trip'
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.title, 'Partially Updated Trip')

    def test_delete_trip(self):
        """Test: deleting a trip"""
        url = f'/api/trips/{self.trip.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Trip.objects.count(), 0)

    def test_create_trip_invalid_dates(self):
        """Test: creating a trip with invalid dates"""
        url = '/api/trips/'

        data = {
            'title': 'Invalid Trip',
            'start_date': date.today() + timedelta(days=20),
            'end_date': date.today() + timedelta(days=10),  # Earlier than start date
            'base_currency': 'USD'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_other_user_cannot_access_trip(self):
        """Test: other user cannot access another user's trip"""
        self.client.force_authenticate(user=self.other_user)

        url = f'/api/trips/{self.trip.id}/'
        response = self.client.get(url)

        # Can be 404 or 403 depending on settings
        self.assertIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]
        )

    def test_other_user_cannot_update_trip(self):
        """Test: other user cannot update another user's trip"""
        self.client.force_authenticate(user=self.other_user)

        url = f'/api/trips/{self.trip.id}/'
        data = {'title': 'Hacked Trip'}
        response = self.client.patch(url, data, format='json')

        self.assertIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]
        )

    def test_other_user_cannot_delete_trip(self):
        """Test: other user cannot delete another user's trip"""
        self.client.force_authenticate(user=self.other_user)

        url = f'/api/trips/{self.trip.id}/'
        response = self.client.delete(url)

        self.assertIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]
        )
        self.assertEqual(Trip.objects.count(), 1)


class TripWithoutAuthTestCase(APITestCase):
    """Tests without authentication"""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.trip = Trip.objects.create(
            user=self.user,
            title="Test Trip",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )

    def test_unauthorized_list_access(self):
        """Test: unauthorized access to list"""
        url = '/api/trips/'
        response = self.client.get(url)

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )

    def test_unauthorized_create(self):
        """Test: creation without authorization"""
        url = '/api/trips/'
        data = {
            'title': 'New Trip',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=7),
        }
        response = self.client.post(url, data, format='json')

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )