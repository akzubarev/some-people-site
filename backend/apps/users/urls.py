from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TokenViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("token", TokenViewSet)
urlpatterns = router.urls
