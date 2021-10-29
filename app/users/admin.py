from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """유저 어드민 화면용 설정"""

    ordering = ["id"]
    fieldsets = (
        (
            "Custom Profile",
            {
                "fields": (
                    "email",
                    "name",
                    "password",
                ),
            },
        ),
    )
    exclude = ("last_name", "first_name", "date_joined")

    list_filter = UserAdmin.list_filter + ("name",)

    ordering = ("email", "name")

    list_display = ("email", "name", "is_staff", "is_superuser")
