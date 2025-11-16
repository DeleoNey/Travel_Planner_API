from rest_framework import routers
from trips import views

router = routers.DefaultRouter()
router.register(r'', views.TripsViewSet)
urlpatterns = router.urls