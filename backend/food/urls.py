from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (IngredientViewSet, RecipeFavoriteViewSet, RecipeViewSet,
                    TagViewSet)

router = SimpleRouter()
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
router.register(r"recipes/(?P<recipe_id>\d+)/favorite", RecipeFavoriteViewSet)
router.register("recipes", RecipeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
