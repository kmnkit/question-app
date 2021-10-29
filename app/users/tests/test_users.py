import json
import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

user_list_url = reverse("users:user-list")
signup_url = reverse("users:signup")

_user_payload = {"email": "admin@admin.com", "name": "admin123", "password": "admin123"}


@pytest.fixture
def ready_a_user(client, django_user_model):
    """테스트용 유저 셋업"""
    user = django_user_model.objects.create(
        email=_user_payload["email"],
        name=_user_payload["name"],
    )
    user.set_password(_user_payload["password"])
    user.save()
    yield user


def test_signup_should_succeed_and_allowed_any(client):
    """
    테스트 1) 이메일,이름,비밀번호로 회원을 작성했을 때 성공해야 한다.(상태코드 201)
    테스트 2) 돌아온 리스트의 첫번째 오브젝트의 이름이 페이로드의 이름과 같아야 한다.
    테스트 3) 돌아온 리스트의 첫번째 오브젝트의 이메일이 페이로드의 이메일과 같아야 한다.
    """
    response = client.post(signup_url, data=_user_payload)
    response_content = json.loads(response.content)

    assert response.status_code == status.HTTP_201_CREATED  # 테스트 1
    assert response_content.get("name") == _user_payload["name"]  # 테스트 2
    assert response_content.get("email") == _user_payload["email"]  # 테스트 3


def test_get_user_list_without_token_should_failed(client):
    """
    테스트 1) 유저를 작성하지 않은 상태에서 리스트 취득불가(상태코드 401)
    테스트 2) 돌아온 리스트가 빈 리스트
    """
    response = client.get(user_list_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # 테스트 1


def test_create_user_by_already_exists_email_should_failed(client, ready_a_user):
    """
    테스트 1) 이미 생성된 유저와 같은 이메일로 유저 생성이 되지 않아야 한다.
    """
    # client.post(path=users_url, data=payload)  # payload로 유저를 한 번 생성
    # payload와 같은 이메일로 한 번 더 유저 작성을 시도한다.
    response = client.post(
        path=signup_url,
        data={
            "email": _user_payload["email"],
            "name": "awesomeuser",
            "password": _user_payload["password"],
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST  # 테스트 1


def test_create_user_by_already_exists_name_should_failed(client, ready_a_user):
    """
    테스트 1) 이미 생성된 유저와 같은 이름으로 유저 생성이 되지 않아야 한다.
    """
    # payload와 같은 이름으로 한 번 더 유저 작성을 시도한다.
    response = client.post(
        path=signup_url,
        data={
            "email": "admin1@aiffel.com",
            "name": _user_payload["name"],
            "password": _user_payload["password"],
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST  # 테스트 1
