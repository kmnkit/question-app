from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView


class CreateUserView(CreateAPIView):
    """회원가입 뷰"""

    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "login":
            return UserLoginSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == "login":
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
