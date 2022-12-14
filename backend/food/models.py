from django.core.validators import MinValueValidator
from django.db import models


class Ingredient(models.Model):
    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    name = models.CharField(
        db_index=True,
        max_length=200,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единицы измерения",
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="Цвет в HEX",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL",
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    class Meta:
        ordering = ("-id",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    tag = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name="Тег",
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        related_name="recipes",
        verbose_name="Ингредиент",
    )
    name = models.CharField(
        db_index=True,
        max_length=200,
        verbose_name="Название",
    )
    image = models.ImageField(
        "Картинка",
        upload_to="recipes/",
    )
    text = models.TextField(
        verbose_name="Описание",
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message="Время приготовления не может быть меньше 1"
            ),
        ],
        verbose_name="Время приготовления (в минутах)",
    )

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe: Recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipe",
    )
    ingredient: Ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipe",
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Количество не может быть меньше 1"),
        ],
        verbose_name="Количество",
    )

    def __str__(self):
        return (
            f"{self.recipe.name} - {self.ingredient.name} "
            f"({self.amount} {self.ingredient.measurement_unit}) "
        )
