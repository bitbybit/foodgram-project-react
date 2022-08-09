from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .filtersets import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from .pagination import PageNumberLimitPagination
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeFavoriteSerializer,
                          RecipeSerializer, RecipeSerializerWrite,
                          TagSerializer)
from .viewsets import CreateDestroyModelViewSet


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


class RecipeFavoriteViewSet(CreateDestroyModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RecipeFavoriteSerializer

    def get_object(self) -> Recipe:
        return get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))

    def is_favorited(self) -> bool:
        recipe = self.get_object()

        return self.request.user.favorite.filter(id=recipe.id).exists()

    @staticmethod
    def error(text: str) -> Response:
        return Response(
            {
                "errors": text,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def create(self, request, *args, **kwargs):
        if self.is_favorited():
            return self.error("Рецепт уже есть в избранном")

        recipe = self.get_object()

        serializer = self.get_serializer(instance=recipe)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer: RecipeFavoriteSerializer):
        recipe = self.get_object()

        self.request.user.favorite.add(recipe)
        self.request.user.save()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self.is_favorited():
            return self.error("Рецепта не было в избранном")

        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance: Recipe):
        self.request.user.favorite.remove(instance)
        self.request.user.save()
