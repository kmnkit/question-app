from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("questions/", include("questions.urls", namespace="questions")),
    path("api/token/", obtain_jwt_token),  # JWT 토큰 발행시 사용
    path("api/token/verify/", verify_jwt_token),  # JWT 토큰이 유효한지 검증할 때 사용
    path("api/token/refresh/", refresh_jwt_token),  #  JWT 토큰을 갱신할 때 사용
]
