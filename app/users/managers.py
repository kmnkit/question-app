import re
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, email=None, password=None, **extra_fields):
        """새 유저 생성 함수"""
        if not name:
            raise ValueError("유저 등록에 이름이 반드시 필요합니다.")
        if not email:
            raise ValueError("유저 등록에 이메일이 반드시 필요합니다.")
        if not re.match("[0-9a-z]{6,20}", name):
            raise ValueError("유저명은 영문자와 숫자의 조합으로 6글자 이상 20자 이하여야 합니다.")
        user = self.model(email=self.normalize_email(email), name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email=None, password=None):
        """슈퍼유저 생성 함수"""
        user = self.create_user(name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
