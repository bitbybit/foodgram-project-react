# Generated by Django 2.2.16 on 2022-08-06 10:21
from typing import List

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: List = []

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=200, verbose_name="Название"
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(
                        max_length=200, verbose_name="Единицы измерения"
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиент",
            },
        ),
        migrations.CreateModel(
            name="IngredientInRecipe",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="Количество не может быть меньше 1"
                            )
                        ],
                        verbose_name="Количество",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Название"),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="recipes/", verbose_name="Картинка"
                    ),
                ),
                ("text", models.TextField(verbose_name="Описание")),
                (
                    "cooking_time",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1,
                                message="Время приготовления не может быть "
                                "меньше 1",
                            )
                        ],
                        verbose_name="Время приготовления (в минутах)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рецепт",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        max_length=7, unique=True, verbose_name="Цвет в HEX"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200, unique=True, verbose_name="URL"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
            },
        ),
    ]