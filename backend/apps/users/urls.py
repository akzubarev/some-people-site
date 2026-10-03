"""Users urls."""
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views.session import BrowserRegistration, BrowserSession
from .views.google import GoogleChallengeView, GoogleCredentialView, GoogleIdentityView

from .views import TokenViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("token", TokenViewSet)
urlpatterns = [
    path('session/google/', GoogleCredentialView.as_view()),
    path('session/google/challenge/', GoogleChallengeView.as_view()),
    path('session/google/identity/', GoogleIdentityView.as_view()),
    path('session/', BrowserSession.as_view()),
    path('session/register/', BrowserRegistration.as_view()),
] + router.urls
