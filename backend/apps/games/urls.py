"""Games urls."""
from rest_framework.routers import DefaultRouter

from .views import ApplicationsViewSet, GameViewSet, QuestionsViewSet

router = DefaultRouter()

router.register("games", GameViewSet)
router.register("questions", QuestionsViewSet)
router.register("applications", ApplicationsViewSet)
urlpatterns = router.urls
