from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_nested import routers

from route_points.views import TripPointViewSet
from trips.views import TripsViewSet

router = routers.DefaultRouter()
router.register(r"trips", TripsViewSet, basename="trips")

schema_view = get_schema_view(
    openapi.Info(
        title="Store API",
        default_version='v1',
        description="Store API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

trip_points_router = routers.NestedDefaultRouter(
    router,
    r"trips",
    lookup="trip"
)
trip_points_router.register(
    r"points",
    TripPointViewSet,
    basename="trip-points"
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/trips/', include('trips.urls')),
    path('api/trips/', include('route_points.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
