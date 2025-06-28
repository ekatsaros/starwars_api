from rest_framework import serializers

from ..models import ApiUser


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "password",
        ]

    # hash password field before saving to database
    def create(self, validated_data: dict) -> ApiUser:
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
        ]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
