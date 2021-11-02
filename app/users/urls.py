from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, UserListViewSet, UserDetailViewSet

app_name = "users"

users_router = DefaultRouter()

urlpatterns = [
    path("", UserListViewSet.as_view(), name="list"),
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("<int:pk>/", UserDetailViewSet.as_view(), name="detail"),
]
urlpatterns += users_router.urls
