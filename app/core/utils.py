from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response(
            {"error": "You are unauthorized to make this request."}, status=401
        )
    return exception_handler(exc, context)