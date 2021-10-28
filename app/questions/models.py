from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(TimeStampedModel):
    """질문 모델"""

    author = models.ForeignKey(User, related_name="questions", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    text = models.TextField(max_length=1000, null=False, blank=False)
    nice_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s by %s" % (self.title, self.author)

    def add_nice_count(self):
        self.nice_count += 1

    def remove_nice_count(self):
        self.nice_count -= 1 if self.nice_count > 0 else 0

    def get_comment_count(self):
        return self.comments.count()


class Comment(TimeStampedModel):
    """질문에 대한 댓글 모델. 대댓글 작성 가능"""

    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, related_name="comments", on_delete=models.CASCADE
    )
    parent_comment = models.ForeignKey(
        "self",
        related_name="child_comments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    text = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return "%s by %s" % (self.text, self.author)


class Nice(TimeStampedModel):
    """질문에 대한 좋아요 모델. 좋아요/취소 가능"""

    user = models.OneToOneField(User, related_name="nice", on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, related_name="nice", blank=True)

    def __str__(self):
        return "%s user's like list" % self.user.name
