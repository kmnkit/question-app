from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CreateUserView

app_name = "users"

users_router = DefaultRouter()
users_router.register("", UserViewSet)

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
]
urlpatterns += users_router.urls
