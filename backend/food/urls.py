from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (IngredientViewSet, RecipeCartDownloadView,
                    RecipeCartViewSet, RecipeFavoriteViewSet, RecipeViewSet,
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
    r"recipes/(?P<recipe_id>\d+)/shopping_cart",
    RecipeCartViewSet,
    basename="recipe-cart",
)
router.register(
    "recipes",
    RecipeViewSet,
    basename="recipe",
)

urlpatterns = [
    path("recipes/download_shopping_cart/", RecipeCartDownloadView.as_view()),
    path("", include(router.urls)),
]
