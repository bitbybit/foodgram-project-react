from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


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


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )
    name = serializers.ReadOnlyField(source="ingredient.name")

    class Meta:
        fields = (
            "amount",
            "id",
            "measurement_unit",
            "name",
        )

        model = IngredientInRecipe


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        required=True,
        source="tag",
    )
    author = UserSerializer(
        required=True,
    )
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source="ingredientinrecipe_set",
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj: Recipe) -> bool:
        user = self.context.get("request").user

        if not user.is_authenticated:
            return False

        return user.favorite.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        user = self.context.get("request").user

        if not user.is_authenticated:
            return False

        return user.cart.filter(id=obj.id).exists()

    class Meta:
        fields = (
            "author",
            "cooking_time",
            "id",
            "image",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "tags",
            "text",
        )

        model = Recipe
