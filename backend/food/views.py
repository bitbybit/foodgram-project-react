from api.pagination import PageNumberLimitPagination
from api.viewsets import PdfView, SwitchOnOffViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .filtersets import IngredientFilter, RecipeFilter
from .helpers import get_unique_recipe_ingredients
from .models import Ingredient, Recipe, Tag
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCompactSerializer,
                          RecipeSerializer, RecipeSerializerWrite,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    pagination_class = PageNumberLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in (
            "create",
            "partial_update",
            "update",
        ):
            return RecipeSerializerWrite
        return RecipeSerializer


class RecipeFavoriteViewSet(SwitchOnOffViewSet):
    model_class = Recipe
    serializer_class = RecipeCompactSerializer
    router_pk = "recipe_id"
    error_text_create = "Рецепт уже есть в избранном"
    error_text_destroy = "Рецепта не было в избранном"

    def is_on(self) -> bool:
        recipe = self.get_object()

        return self.request.user.favorite.filter(id=recipe.id).exists()

    def perform_create(self, serializer: RecipeCompactSerializer):
        recipe = self.get_object()

        self.request.user.favorite.add(recipe)
        self.request.user.save()

    def perform_destroy(self, instance: Recipe):
        self.request.user.favorite.remove(instance)
        self.request.user.save()


class RecipeCartViewSet(SwitchOnOffViewSet):
    model_class = Recipe
    serializer_class = RecipeCompactSerializer
    router_pk = "recipe_id"
    error_text_create = "Рецепт уже есть в списке покупок"
    error_text_destroy = "Рецепта не было в списке покупок"

    def is_on(self) -> bool:
        recipe = self.get_object()

        return self.request.user.cart.filter(id=recipe.id).exists()

    def perform_create(self, serializer: RecipeCompactSerializer):
        recipe = self.get_object()

        self.request.user.cart.add(recipe)
        self.request.user.save()

    def perform_destroy(self, instance: Recipe):
        self.request.user.cart.remove(instance)
        self.request.user.save()


class RecipeCartDownloadView(PdfView):
    filename = "Список покупок.pdf"

    def get_text_lines(self):
        recipes = self.request.user.cart.all()
        unique_recipe_ingredients = get_unique_recipe_ingredients(recipes)
        text_lines = []

        for ingredient in unique_recipe_ingredients.values():
            text_lines.append(
                f"{ingredient['name']} ({ingredient['unit']}) "
                f"— {ingredient['amount']}"
            )

        return text_lines
