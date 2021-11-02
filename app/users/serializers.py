from rest_framework import serializers as sz
from django.contrib.auth import get_user_model


class UserSerializer(sz.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "name", "password")
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        password = validated_data.get("password")
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


"""
TODO: payload에 유저 ID만 담고 싶었으나,
토큰 발급 이후 verify와 refresh에서 invalid payload 문제가 발생한다.
커스텀은 과제로 두도록 한다.
"""
# class UserLoginSerializer(sz.Serializer):
#     name = sz.CharField(max_length=200)
#     password = sz.CharField(max_length=128, write_only=True)
#     token = sz.CharField(max_length=255, read_only=True)

#     def validate(self, data):
#         name = data.get("name", None)
#         password = data.get("password", None)
#         user = authenticate(name=name, password=password)
#         if user is None:
#             return {"name": "None"}
#         try:
#             payload = api_settings.jwt_payload_handler(user)
#             jwt_token = api_settings.JWT_ENCODE_HANDLER(payload)
#             update_last_login(None, user)
#         except get_user_model().DoesNotExist:
#             raise sz.ValidationError(
#                 "User with given email and password does not exist"
#             )
#         return {"name": user.name, "token": jwt_token}
