from rest_framework import serializers as sz
from .models import Question, Comment, Nice


class QuestionSerializer(sz.ModelSerializer):
    class Meta:
        model = Question
        read_only_fields = (
            "author",
            "nice_count",
        )
        exclude = ("updated_at",)


class CommentSerializer(sz.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("updated_at",)


class NiceSerializer(sz.ModelSerializer):
    class Meta:
        model = Nice
        exclude = ("updated_at",)
