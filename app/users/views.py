from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    """회원가입 뷰"""

    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserListViewSet(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """회원가입을 CreateUserView로 구현하였기에 나머지를 따로 구현함."""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # permission: [IsAuthenticated]
