from django.db import models
from trips.models import Trip


class TripPoint(models.Model):
    trip = models.ForeignKey(Trip, related_name='points', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date = models.DateField()
    planned_budget = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.trip} | {self.city} | {self.country}'