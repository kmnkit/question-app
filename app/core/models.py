from django.db import models


class TimeStampedModel(models.Model):
    """타임스탬프 기록 추상 모델"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
