from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound
from core.permissions import IsOwnerPermission

from .serializers import TripPointSerializer
from trips.models import Trip


class TripPointViewSet(viewsets.ModelViewSet):
    serializer_class = TripPointSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]

    def get_trip(self):
        trip_id = self.kwargs.get("trip_id")
        try:
            return Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
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
