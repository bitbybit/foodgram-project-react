from django.core.validators import MinValueValidator
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=200,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единицы измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"


class Tag(models.Model):
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

    class Meta:
        verbose_name = "Тег"


class Recipe(models.Model):
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

    class Meta:
        verbose_name = "Рецепт"


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Количество не может быть меньше 1"),
        ],
        verbose_name="Количество",
    )
