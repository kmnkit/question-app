from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet

app_name = "questions"

questions_router = DefaultRouter()
questions_router.register("questions", QuestionViewSet)


urlpatterns = questions_router.urls
