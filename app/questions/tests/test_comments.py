import pytest
from django.urls import reverse
from questions.models import Question
from rest_framework import status

pytestmark = pytest.mark.django_db

question_list_url = reverse("questions:question-list")

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
    client.force_login(user)  # 강제 인증
    yield user


@pytest.fixture
def ready_a_question(ready_a_user):
    question = Question.objects.create(
        author=ready_a_user, title="Hey! What's up?", text="I am fine!"
    )
    yield question


def test_get_comments_for_a_question(client, ready_a_question):
    """하나의 질문에 대한 댓글 목록 호출이 성공해야 한다.(권한 상관 없음)"""
    q_id = ready_a_question.id
    response = client.get(
        path="%scomments/" % reverse("questions:question-detail", args=[q_id])
    )
    assert response.status_code == status.HTTP_200_OK


def test_create_comment_for_a_question(client, ready_a_user, ready_a_question):
    """하나의 질문에 대한 댓글 작성이 성공해야 한다. (인증 필요)"""
    q_id = ready_a_question.id
    response = client.post(
        "%sadd-comment/" % reverse("questions:question-detail", args=[q_id]),
        {
            "author": ready_a_user.id,
            "question": q_id,
            "text": "How awesome question! Good luck!",
        },
        format="json",
    )
    assert (
        response.status_code == status.HTTP_200_OK
    )  # detail에 대한 POST라서 201이 아닌 200이 맞음.
