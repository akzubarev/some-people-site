"""Games urls."""
from rest_framework.routers import DefaultRouter
from drf_spectacular.utils import extend_schema, extend_schema_view

from .views import ApplicationsViewSet, GameViewSet, QuestionsViewSet
from .organizer import OrganizerGameViewSet
from .organizer_content import (OrganizerGroupViewSet, OrganizerCharacterViewSet,
                                OrganizerTagViewSet, OrganizerQuestionViewSet, OrganizerMultipartSerializer)
from .organizer_applications import OrganizerApplicationViewSet
from apps.notifications.organizer import OrganizerMailingViewSet

router = DefaultRouter()

router.register("games", GameViewSet)
router.register("questions", QuestionsViewSet)
router.register("applications", ApplicationsViewSet)
router.register("organizer/games", OrganizerGameViewSet, basename="organizer-games")
for resource, view in [('groups', OrganizerGroupViewSet), ('characters', OrganizerCharacterViewSet),
                       ('tags', OrganizerTagViewSet), ('questions', OrganizerQuestionViewSet),
                       ('applications', OrganizerApplicationViewSet), ('mailings', OrganizerMailingViewSet)]:
    view = extend_schema_view(
        create=extend_schema(request={'application/json': view.serializer_class, 'multipart/form-data': OrganizerMultipartSerializer}),
        partial_update=extend_schema(request={'application/json': view.serializer_class, 'multipart/form-data': OrganizerMultipartSerializer}),
    )(view)
    router.register(r'organizer/games/(?P<game_id>[0-9]+)/' + resource, view,
                    basename='organizer-' + resource)
urlpatterns = router.urls
