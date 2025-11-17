import http

from rest_framework import viewsets, permissions, response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from core.permissions import IsOwnerPermission
from rest_framework.response import Response

from .serializers import TripPointSerializer
from route_points.models import TripPoint
from integrations.services.weather import WeatherService

class TripPointViewSet(viewsets.ModelViewSet):
    serializer_class = TripPointSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]

    def get_trip(self):
        trip_id = self.kwargs.get("trip_id")
        try:
            return TripPoint.objects.get(id=trip_id)
        except TripPoint.DoesNotExist:
            raise NotFound("Trip not found")

    def get_queryset(self):
        trip = self.get_trip()
        return trip.points.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['trip'] = self.get_trip()
        return context

    def perform_create(self, serializer):
        serializer.save(trip=self.get_trip())


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = TripPoint.objects.all()
    serializer_class = TripPointSerializer

    def retrieve(self, request, *args, **kwargs):
        trip_point = self.get_object()

        serializer = self.get_serializer(trip_point)
        data = serializer.data

        if trip_point.latitude and trip_point.longitude:
            weather_service = WeatherService()

            current_temp = weather_service.get_weather(
                lat=str(trip_point.latitude),
                lon=str(trip_point.longitude)
            )

            data['weather'] = {
                'current_temp': current_temp,
            }
            if not current_temp:
                return response.Response("Weather not found", status=HTTP_404_NOT_FOUND)

        return Response(data)