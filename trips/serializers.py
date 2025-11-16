from rest_framework import serializers
from trips.models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'base_currency',
            'created_at',
        )
