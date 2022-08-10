from api.fields import ImageBase64Field
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


class IngredientInRecipeSerializerWrite(IngredientInRecipeSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        required=True,
    )

    class Meta:
        fields = (
            "amount",
            "id",
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
        required=True,
        source="ingredient_in_recipe",
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


class RecipeSerializerWrite(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
    )
    ingredients = IngredientInRecipeSerializerWrite(
        many=True,
        required=True,
    )
    image = ImageBase64Field(required=True)

    def process_data(self, validated_data, instance=None):
        validated_data["author"] = self.context.get("request").user

        try:
            tags = validated_data.pop("tags")
        except KeyError:
            tags = []

        try:
            ingredients = validated_data.pop("ingredients")
        except KeyError:
            ingredients = []

        if instance is None:
            recipe = Recipe.objects.create(**validated_data)
        else:
            recipe = instance

            for attr, value in validated_data.items():
                setattr(recipe, attr, value)

        if tags:
            recipe.tag.clear()

            for tag_item in tags:
                recipe.tag.add(tag_item)

        if ingredients:
            recipe.ingredient.clear()

            for ingredient_item in ingredients:
                recipe.ingredient.add(
                    ingredient_item["id"],
                    through_defaults={"amount": ingredient_item["amount"]},
                )

        recipe.save()

        return recipe

    def create(self, validated_data):
        return self.process_data(validated_data)

    def update(self, instance, validated_data):
        return self.process_data(validated_data, instance)

    def to_representation(self, obj: Recipe):
        serializer = RecipeSerializer(instance=obj, context=self.context)
        return serializer.data

    class Meta:
        fields = (
            "cooking_time",
            "image",
            "ingredients",
            "name",
            "tags",
            "text",
        )

        model = Recipe


class RecipeCompactSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "cooking_time",
            "id",
            "image",
            "name",
        )

        model = Recipe
