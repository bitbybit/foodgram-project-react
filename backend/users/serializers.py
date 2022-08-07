from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj: User) -> bool:
        return obj.following.filter(
            id=self.context.get("request").user.id
        ).exists()

    class Meta:
        fields = (
            "email",
            "first_name",
            "id",
            "is_subscribed",
            "last_name",
            "username",
        )

        model = User


class AuthUserTokenSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user

    def to_representation(self, obj: User):
        self.fields.pop("password")

        return super().to_representation(obj)

    class Meta:
        fields = (
            "email",
            "first_name",
            "id",
            "last_name",
            "password",
            "username",
        )

        model = User
