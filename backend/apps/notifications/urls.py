from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, TelegramView, MailingViewSet
from django.urls import path


router = DefaultRouter()

router.register('notifications', NotificationViewSet)
# router.register('telegram', TelegramMetaView)
urlpatterns = router.urls
urlpatterns += [
    path('telegram/', TelegramView.as_view()),
]
urlpatterns += [
    path('mailing/', MailingViewSet.as_view()),
]