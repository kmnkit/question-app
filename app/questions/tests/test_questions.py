import json
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from questions.models import Question

pytestmark = pytest.mark.django_db

User = get_user_model()

user_list_url = reverse("users:user-list")
question_list_url = reverse("questions:question-list")

_user_payload = {"email": "admin@admin.com", "name": "admin123", "password": "admin123"}


@pytest.fixture
def ready_a_user(client):
    """테스트용 유저 셋업 후 강제 인증 시킨다."""
    user = get_user_model().objects.create(
        email=_user_payload["email"],
        name=_user_payload["name"],
    )
    user.set_password(_user_payload["password"])
    user.save()
    client.force_login(user)
    yield user


def test_no_question_object_should_return_empty_list(client, ready_a_user) -> None:
    """
    아무 질문 데이터가 없는 상태에서도 정상적인 API 호출이 가능한지 테스트한다.
    테스트 1) 정상적인 API 호출이 가능하다.(status 200)
    테스트 2) 아무 질문도 작성하지 않은 상태에서의 질문 리스트는 빈 리스트여야 한다.
    """
    response = client.get(path=question_list_url)
    response_content = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert response_content == []


def test_get_questions_with_keyword_should_succees(client, ready_a_user) -> None:
    """
    키워드 파라미터(keyword)라는 키워드로 질문 검색이 가능해야 한다.
    2건을 작성하며, 각각 제목에 Today, 내용에 Tomorrow가 각각 대소문자 시작, 제목과 내용에 각각 sunny라는 단어가 들어가 있다.
    keyword parameter 검색은 대소문자 구별 없이 제목, 내용에 포함되어 있는 것을 찾는다.
    """
    Question.objects.create(
        **{
            "author": ready_a_user,
            "title": "Today is Sunny",
            "text": "Tomorrow will Rainy",
        }
    )
    Question.objects.create(
        **{
            "author": ready_a_user,
            "title": "Today is Cloudy",
            "text": "Maybe tomorrow will Sunny",
        }
    )
    # Today 키워드 검색
    path = "%s?%s" % (question_list_url, "keyword=Today")
    response = client.get(path=path)
    response_content = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert len(response_content) == 2

    # Tomorrow 키워드 검색
    path = "%s?%s" % (question_list_url, "keyword=Tomorrow")
    response = client.get(path=path)
    response_content = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert len(response_content) == 2

    # Sunny 키워드 검색(전체 소문자)
    path = "%s?%s" % (question_list_url, "keyword=sunny")
    response = client.get(path=path)
    response_content = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert len(response_content) == 2


def test_creating_a_question_should_succeed(client, ready_a_user) -> None:
    """질문이 정상적으로 작성된다."""
    response = client.post(
        path=question_list_url,
        data={"author": ready_a_user.id, "title": "Are you hungry?", "text": "Really?"},
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_editing_a_question_should_succeed(client, ready_a_user) -> None:
    """질문 수정이 정상적으로 작동한다."""
    question_payload = {
        "author": ready_a_user,
        "title": "Are you hungry?",
        "text": "Really?",
    }
    question = Question.objects.create(**question_payload)
    response = client.put(
        path=reverse("questions:question-detail", args=[question.id]),
        data={
            "author": ready_a_user.id,
            "title": "Hello, i want to edit this question",
            "text": "Bye, I edited this question!",
        },
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK


def test_deleting_a_question_should_succeed(client, ready_a_user) -> None:
    """질문 삭제가 성공해야 한다."""
    question_payload = {
        "author": ready_a_user,
        "title": "Are you hungry?",
        "text": "Really?",
    }
    question = Question.objects.create(**question_payload)
    response = client.delete(
        path=reverse("questions:question-detail", args=[question.id]),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_deleting_other_peoples_question_should_failed(client, ready_a_user) -> None:
    """다른 사람의 질문을 삭제할 수 없다는 테스트"""
    # 질문내용 하나 준비
    question_payload = {
        "author": ready_a_user,
        "title": "Are you hungry?",
        "text": "Really?",
    }
    # 현재 로그인 된 유저로 질문 작성
    question = Question.objects.create(**question_payload)
    client.logout()
    # 새 유저 작성
    new_user = User.objects.create(email="other@admin.com", name="other123")
    new_user.set_password("other123")
    new_user.save()
    # 새로 작성한 유저 강제 로그인
    client.force_login(new_user)
    response = client.delete(
        path=reverse("questions:question-detail", args=[question.id]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
