"""Urls configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

admin.site.enable_nav_sidebar = False
admin.site.site_header = "Какие-то люди"
admin.site.site_title = "Какие-то люди: Админ панель"
admin.site.index_title = "Какие-то люди: Админ панель"

router = routers.DefaultRouter()

urlpatterns = [
    # Admin
    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # API
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.notifications.urls')),
    path('api/', include('apps.games.urls')),
]

# DEV
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
