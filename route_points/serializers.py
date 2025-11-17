from rest_framework import serializers
from .models import TripPoint


class TripPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripPoint
        fields = '__all__'
        read_only_fields = ['trip']

    def validate(self, attrs):
        trip = self.context['trip']
        visit_date = attrs.get('date')

        if visit_date:
            if visit_date < trip.start_date or visit_date > trip.end_date:
                raise serializers.ValidationError(
                    f"visit_date must be between {trip.start_date} and {trip.end_date}"
                )

        lat = attrs.get('latitude')
        lon = attrs.get('longitude')

        if lat and not (-90 <= float(lat) <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90")

        if lon and not (-180 <= float(lon) <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180")

        return attrs
