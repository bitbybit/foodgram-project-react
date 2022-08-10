import importlib
from typing import Dict

from django.db.models import Count
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context.get("request").user

        if not user.is_authenticated:
            return False

        return obj.following.filter(id=user.id).exists()

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


class SubscribedUserSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj: User) -> Dict:
        recipes_limit = int(
            self.context.get("request").GET.get("recipes_limit", default=0)
        )

        if recipes_limit > 0:
            recipes = obj.recipes.all()[:recipes_limit]
        else:
            recipes = obj.recipes.all()

        serializer_class = getattr(
            importlib.import_module("food.serializers"),
            "RecipeCompactSerializer",
        )
        serializer = serializer_class(
            many=True,
            instance=recipes,
        )

        return serializer.data

    @staticmethod
    def get_recipes_count(obj: User) -> int:
        return obj.recipes.aggregate(Count("id"))["id__count"]

    class Meta:
        fields = (
            "email",
            "first_name",
            "id",
            "is_subscribed",
            "last_name",
            "recipes",
            "recipes_count",
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
