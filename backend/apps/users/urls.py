"""Users urls."""
from rest_framework.routers import DefaultRouter

from .views import TokenViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("token", TokenViewSet)
urlpatterns = router.urls
