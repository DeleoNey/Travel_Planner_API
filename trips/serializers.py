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


    def validate(self, attrs):
        start = attrs.get('start_date')
        end = attrs.get('end_date')
        if start and end and end < start:
            raise serializers.ValidationError({
                'end_date': "End date cannot be earlier than start date."
            })
        return attrs