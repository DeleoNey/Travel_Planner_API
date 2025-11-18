from rest_framework import viewsets, permissions, response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response

from core.permissions import IsOwnerPermission
from integrations.services.places import PlacesService

from .serializers import TripPointSerializer
from route_points.models import TripPoint
from trips.models import Trip
from integrations.services.weather import WeatherService
from travel_planner_api import settings


class TripPointViewSet(viewsets.ModelViewSet):
    serializer_class = TripPointSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]

    def get_trip(self):
        trip_id = self.kwargs.get("trip_id")
        if not trip_id:
            return None
        try:
            return Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            raise NotFound("Trip not found")

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return TripPoint.objects.none()

        trip = self.get_trip()
        if trip is None:
            return TripPoint.objects.none()
        return trip.points.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        trip = self.get_trip()
        if trip is not None:
            context['trip'] = trip
        return context

    @action(detail=True, methods=["get"], url_path="places-nearby")
    def places_nearby(self, request, trip_id=None, pk=None):
        point = self.get_object()  # TripPoint instance

        # ініціалізуємо сервіс
        places_service = PlacesService(settings.PLACES_API_KEY)

        # викликаємо API
        data = places_service.get_nearby_places(
            lat=point.latitude,
            lon=point.longitude,
            radius=10,
            categories="tourism.sights"
        )

        return Response(data)

    def perform_create(self, serializer):
        trip = self.get_trip()
        if trip is None:
            raise NotFound("Trip not found")
        serializer.save(trip=trip)


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = TripPoint.objects.all()
    serializer_class = TripPointSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]

    def retrieve(self, request, *args, **kwargs):
        trip_point = self.get_object()

        serializer = self.get_serializer(trip_point)
        data = serializer.data

        if trip_point.latitude and trip_point.longitude:
            weather_service = WeatherService()

            weather_metrics = weather_service.get_weather(
                lat=str(trip_point.latitude),
                lon=str(trip_point.longitude),
            )

            data['weather'] = weather_metrics

            if 'error' in data['weather']:
                return Response("Weather not found", status=HTTP_404_NOT_FOUND)

        return Response(data)