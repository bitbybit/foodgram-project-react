from rest_framework import serializers

from .models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "color",
            "id",
            "name",
            "slug",
        )

        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "measurement_unit",
            "name",
        )

        model = Ingredient
