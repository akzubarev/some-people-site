"""Notification urls."""
from rest_framework.routers import DefaultRouter

from .views import NotificationViewSet

router = DefaultRouter()

router.register('notifications', NotificationViewSet)
urlpatterns = router.urls
urlpatterns += [
    # path('mailing/', MailingViewSet.as_view()),
]
