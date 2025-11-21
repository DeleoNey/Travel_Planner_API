from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch

from trips.models import Trip
from route_points.models import TripPoint

User = get_user_model()


class TripPointCRUDTestCase(APITestCase):
    """Tests for CRUD operations on trip points"""

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
            email='othertestemail@gmail.com',
        )

        self.trip = Trip.objects.create(
            user=self.user,
            title="Test Trip",
            description="Test description",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            base_currency='USD'
        )

        self.other_trip = Trip.objects.create(
            user=self.other_user,
            title="Other Trip",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
        )

        self.trip_point = TripPoint.objects.create(
            trip=self.trip,
            city="Kyiv",
            country="Ukraine",
            date=date.today() + timedelta(days=1),
            planned_budget=Decimal("100.00"),
            latitude=50.4501,
            longitude=30.5234
        )

        self.client.force_authenticate(user=self.user)

    def test_get_trip_points_list(self):
        """Test: retrieving list of trip points"""
        url = f'/api/trips/{self.trip.id}/points/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check pagination
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['city'], 'Kyiv')
            self.assertIn('local_budget', response.data['results'][0])
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['city'], 'Kyiv')
            self.assertIn('local_budget', response.data[0])

    def test_create_trip_point(self):
        """Test: creating a new trip point"""
        url = f'/api/trips/{self.trip.id}/points/'

        data = {
            'city': 'Lviv',
            'country': 'Ukraine',
            'date': date.today() + timedelta(days=2),
            'planned_budget': '150.00',
            'latitude': 49.8397,
            'longitude': 24.0297
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TripPoint.objects.filter(trip=self.trip).count(), 2)
        self.assertEqual(response.data['city'], 'Lviv')

    def test_get_trip_point_detail(self):
        """Test: retrieving details of a single trip point"""
        url = f'/api/trips/{self.trip.id}/points/{self.trip_point.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], 'Kyiv')
        self.assertEqual(float(response.data['planned_budget']), 100.00)
        self.assertIn('local_budget', response.data)

    def test_update_trip_point(self):
        """Test: updating a trip point"""
        url = f'/api/trips/{self.trip.id}/points/{self.trip_point.id}/'

        data = {
            'city': 'Kyiv Updated',
            'country': 'Ukraine',
            'date': self.trip_point.date,
            'planned_budget': '200.00',
            'latitude': self.trip_point.latitude,
            'longitude': self.trip_point.longitude
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_point.refresh_from_db()
        self.assertEqual(self.trip_point.city, 'Kyiv Updated')
        self.assertEqual(float(self.trip_point.planned_budget), 200.00)

    def test_partial_update_trip_point(self):
        """Test: partially updating a trip point"""
        url = f'/api/trips/{self.trip.id}/points/{self.trip_point.id}/'

        data = {
            'city': 'Kyiv Partial Update'
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip_point.refresh_from_db()
        self.assertEqual(self.trip_point.city, 'Kyiv Partial Update')

    def test_delete_trip_point(self):
        """Test: deleting a trip point"""
        url = f'/api/trips/{self.trip.id}/points/{self.trip_point.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TripPoint.objects.filter(trip=self.trip).count(), 0)

    def test_invalid_date_validation(self):
        """Test: validating date outside of trip range"""
        url = f'/api/trips/{self.trip.id}/points/'

        data = {
            'city': 'Odesa',
            'country': 'Ukraine',
            'date': date.today() + timedelta(days=30),  # outside trip
            'planned_budget': '100.00',
            'latitude': 46.4825,
            'longitude': 30.7233
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_coordinates(self):
        """Test: validating invalid coordinates"""
        url = f'/api/trips/{self.trip.id}/points/'

        data = {
            'city': 'Test',
            'country': 'Test',
            'date': date.today() + timedelta(days=1),
            'planned_budget': '100.00',
            'latitude': 999,  # invalid latitude
            'longitude': 30.0
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_trip_not_found(self):
        """Test: request for a non-existent trip"""
        url = '/api/trips/99999/points/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_user_cannot_access_points(self):
        """Test: another user cannot access someone else's points"""
        self.client.force_authenticate(user=self.other_user)

        url = f'/api/trips/{self.trip.id}/points/'
        response = self.client.get(url)

        # May return empty list or 403/404
        if response.status_code == status.HTTP_200_OK:
            if 'results' in response.data:
                self.assertEqual(len(response.data['results']), 0)
            else:
                self.assertEqual(len(response.data), 0)
        else:
            self.assertIn(
                response.status_code,
                [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]
            )

    @patch('integrations.services.currency.CurrencyService.convert_budget_for_country')
    def test_local_budget_calculation_with_mock(self, mock_convert):
        """Test: calculating local_budget using mock"""
        mock_convert.return_value = {
            'converted_amount': 4000.00,
            'currency': 'UAH'
        }

        url = f'/api/trips/{self.trip.id}/points/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            local_budget = response.data['results'][0]['local_budget']
        else:
            local_budget = response.data[0]['local_budget']

        # Check that local_budget exists
        self.assertIsNotNone(local_budget)
        mock_convert.assert_called()


class TripPointPlacesNearbyTestCase(APITestCase):
    """Tests for nearby places search"""

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

        self.trip_point = TripPoint.objects.create(
            trip=self.trip,
            city="Kyiv",
            country="Ukraine",
            date=date.today() + timedelta(days=1),
            planned_budget=Decimal("100.00"),
            latitude=50.4501,
            longitude=30.5234
        )

        self.client.force_authenticate(user=self.user)

    @patch('integrations.services.places.PlacesService.get_nearby_places')
    def test_get_places_nearby(self, mock_places):
        """Test: retrieving nearby places"""
        mock_places.return_value = {
            'places': [
                {'name': 'Test Place 1', 'type': 'museum'},
                {'name': 'Test Place 2', 'type': 'restaurant'}
            ]
        }

        url = f'/api/trips/{self.trip.id}/points/{self.trip_point.id}/places-nearby/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('places', response.data)
        mock_places.assert_called_once()


class TripPointWeatherTestCase(APITestCase):
    """Tests for retrieving weather"""

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

        self.trip_point = TripPoint.objects.create(
            trip=self.trip,
            city="Kyiv",
            country="Ukraine",
            date=date.today() + timedelta(days=1),
            planned_budget=Decimal("100.00"),
            latitude=50.4501,
            longitude=30.5234
        )

        self.client.force_authenticate(user=self.user)

    @patch('integrations.services.weather.WeatherService.get_weather')
    def test_get_weather(self, mock_weather):
        """Test: retrieving weather for a trip point"""
        mock_weather.return_value = {
            'temperature': 20,
            'description': 'Clear sky'
        }

        url = f'/api/trips/{self.trip.id}/points/{self.trip_point.id}/weather/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('weather', response.data)
        mock_weather.assert_called_once()
