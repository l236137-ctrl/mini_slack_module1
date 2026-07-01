from django.contrib import admin
from django.urls import path

from core.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health", health_check, name="health-check"),
    # Module 2+ will add, e.g.:
    # path("api/v1/", include("accounts.urls")),
]
