from django.contrib import admin
from django.db.models import Count

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
    )
    list_filter = (
        "author",
        "name",
        "tag",
    )

    readonly_fields = ("favorited",)

    def favorited(self, instance: Recipe) -> int:
        return instance.users_favorited.aggregate(Count("id"))["id__count"]

    favorited.short_description = "Общее число добавлений рецепта в избранное"


admin.site.register(Tag)
admin.site.register(IngredientInRecipe)
