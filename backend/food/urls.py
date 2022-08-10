from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (IngredientViewSet, RecipeFavoriteViewSet, RecipeViewSet,
                    TagViewSet)

router = SimpleRouter()
router.register(
    "tags",
    TagViewSet,
    basename="tag",
)
router.register(
    "ingredients",
    IngredientViewSet,
    basename="ingredient",
)
router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite",
    RecipeFavoriteViewSet,
    basename="recipe-favorite",
)
router.register(
    "recipes",
    RecipeViewSet,
    basename="recipe",
)

urlpatterns = [
    path("", include(router.urls)),
]
