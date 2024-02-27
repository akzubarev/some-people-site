from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path
from django.shortcuts import redirect
from .views import TokenCreateView, TokenDestroyView

router = DefaultRouter()
router.register("users", UserViewSet)
urlpatterns = router.urls


def refer(request, rid):
    response = redirect("/?r=" + str(rid))
    response.set_cookie("refer", rid)
    return response


urlpatterns += [path("r/<int:rid>/", refer)]

urlpatterns += [
    path("token/login/", TokenCreateView.as_view(), name="login"),
    path("token/logout/", TokenDestroyView.as_view(), name="logout"),
]
