from rest_framework import serializers

from integrations.services.currency import CurrencyService
from .models import TripPoint


class TripPointSerializer(serializers.ModelSerializer):
    local_budget = serializers.SerializerMethodField()

    class Meta:
        model = TripPoint
        fields = [
            'id',
            'city',
            'country',
            'date',
            'planned_budget',
            'local_budget',
            'latitude',
            'longitude',
            'created_at',
            'trip',
        ]
        read_only_fields = ['trip', 'local_budget']

    def get_local_budget(self, obj):
        try:
            service = CurrencyService(base_currency="USD")
            converted = service.convert_budget_for_country(
                amount=float(obj.planned_budget),
                country=obj.country
            )
            return converted['converted_amount']
        except Exception:
            return None

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