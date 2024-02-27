from rest_framework.routers import DefaultRouter
from .views import GameViewSet, QuestionsViewSet, ApplicationsViewSet

router = DefaultRouter()

router.register("games", GameViewSet)
router.register("questions", QuestionsViewSet)
router.register("applications", ApplicationsViewSet)
urlpatterns = router.urls
