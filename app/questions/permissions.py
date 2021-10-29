from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission


class IsOwnerOnly(BasePermission):
    # 작성자만 접근
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # 스태프이거나 슈퍼유저의 경우 권한을 가질 수 있다.
            if request.user.is_staff or request.user.is_superuser:
                return True
            # obj의 author가 본인일 경우 권한을 가질 수 있다.
            elif hasattr(obj, "author"):
                return obj.author.id == request.user.id
            return False
        else:
            return False
