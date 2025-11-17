from django.db import models
from travel_planner_api import settings


class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='trips', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    base_currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title