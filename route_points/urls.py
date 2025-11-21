from django.urls import path
from .views import TripPointViewSet, WeatherViewSet

trip_points_list = TripPointViewSet.as_view({
    "get": "list",
    "post": "create",
})

trip_points_detail = TripPointViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

trip_points_places_nearby = TripPointViewSet.as_view({
    "get": "places_nearby",
})

weather_detail = WeatherViewSet.as_view({
    "get": "retrieve",
})

urlpatterns = [
    path(
        "<int:trip_id>/points/",
        trip_points_list,
        name="trip-points-list"
    ),

    path(
        "<int:trip_id>/points/<int:pk>/",
        trip_points_detail,
        name="trip-point-detail"
    ),

    path(
        "<int:trip_id>/points/<int:pk>/places-nearby/",
        trip_points_places_nearby,
        name="trip-point-places-nearby"
    ),

    path(
        "<int:trip_id>/points/<int:pk>/weather/",
        weather_detail,
        name="trip-point-weather"
    ),
]