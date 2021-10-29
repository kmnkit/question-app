import json
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

_user_payload = {"email": "admin@admin.com", "name": "admin12", "password": "admin123"}

pytestmark = pytest.mark.django_db


@pytest.fixture
def ready_a_user():
    """테스트용 유저 셋업 후 강제 인증 시킨다."""
    user = get_user_model().objects.create(
        email=_user_payload["email"],
        name=_user_payload["name"],
    )
    user.set_password(_user_payload["password"])
    user.save()
    yield user


def test_get_token(client, ready_a_user):
    """인증 테스트"""
    response = client.post(
        reverse("core:login"),
        data={
            "name": _user_payload["name"],
            "password": _user_payload["password"],
        },
    )
    assert response.status_code == status.HTTP_200_OK
