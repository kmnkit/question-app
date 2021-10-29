import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("", include("questions.urls", namespace="questions")),
    path("", include("core.urls", namespace="core")),
    path("__debug__/", include(debug_toolbar.urls)),
]
