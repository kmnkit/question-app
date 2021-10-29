from django.contrib import admin
from .models import Question, Comment, Nice


@admin.register(Question)
class CustomQuestionAdmin(admin.ModelAdmin):
    """유저 어드민 화면용 설정"""

    fieldsets = (
        (
            "Custom Profile",
            {
                "fields": (
                    "author",
                    "title",
                    "text",
                    "nice_count",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    list_filter = ("created_at",)

    list_display = (
        "title",
        "nice_count",
        "get_comment_count",
        "created_at",
        "author",
    )

    ordering = ("-nice_count", "-created_at")


@admin.register(Comment)
class CustomCommentAdmin(admin.ModelAdmin):
    """유저 어드민 화면용 설정"""

    fieldsets = (
        (
            "Custom Profile",
            {
                "fields": (
                    "question",
                    "author",
                    "text",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    list_filter = ("created_at",)

    ordering = ("-created_at",)

    list_display = ("text", "created_at", "author")
