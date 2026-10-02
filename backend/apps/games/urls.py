"""Games urls."""
from rest_framework.routers import DefaultRouter

from .views import ApplicationsViewSet, GameViewSet, QuestionsViewSet
from .organizer import OrganizerGameViewSet

router = DefaultRouter()

router.register("games", GameViewSet)
router.register("questions", QuestionsViewSet)
router.register("applications", ApplicationsViewSet)
router.register("organizer/games", OrganizerGameViewSet, basename="organizer-games")
urlpatterns = router.urls
