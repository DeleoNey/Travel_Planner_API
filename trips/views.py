from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwnerPermission
from trips.models import Trip
from trips.serializers import TripSerializer


class TripsViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    queryset = Trip.objects.all()

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)