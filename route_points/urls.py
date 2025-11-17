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
    path("<int:trip_id>/points/<int:pk>/weather/", weather_detail, name="trip-point-weather"),
]


# <int:trip_id>/trips/weather