from django.conf import settings
from django.urls import path, include

from aidants_connect_web.admin import admin_site

urlpatterns = [
    path(settings.ADMIN_URL, admin_site.urls),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("", include("aidants_connect_web.urls")),
]
