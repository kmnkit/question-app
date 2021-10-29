import json
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


def test_add_nice_and_increase_a_nice(client, ready_a_user):
    """질문을 좋아요 추가하면 내가 좋아요 한 목록에 질문 목록에 추가되며 질문의 좋아요 수가 1 증가해야 한다."""

    # 질문 작성
    data = {"author": ready_a_user, "title": "Are you hungry?", "text": "Really?"}
    question = Question.objects.create(**data)
    question_id = question.id
    assert question.get_nice_count() == 0
    response = client.put(
        "%snices/" % reverse("questions:question-detail", args=[question_id]),
        data={"user": ready_a_user.id, "question": question_id},
    )
    assert response.status_code == status.HTTP_200_OK  # 제대로 추가가 완료되었다.
    response = client.get(path=question_list_url, data={"id": question_id})
    response_content = json.loads(response.content)[0]
    assert response_content["nice_count"] == 1  # 질문 오브젝트 재 취득 후 좋아요가 1이 되었다.
    assert question in ready_a_user.nice.questions.all()  # 질문이 유저의 좋아요 한 질문 목록에 있다.
