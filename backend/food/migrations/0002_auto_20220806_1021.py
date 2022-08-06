# Generated by Django 2.2.16 on 2022-08-06 10:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("food", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredient",
            field=models.ManyToManyField(
                related_name="recipes",
                through="food.IngredientInRecipe",
                to="food.Ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tag",
            field=models.ManyToManyField(
                related_name="recipes", to="food.Tag", verbose_name="Тег"
            ),
        ),
        migrations.AddField(
            model_name="ingredientinrecipe",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="food.Ingredient",
            ),
        ),
        migrations.AddField(
            model_name="ingredientinrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="food.Recipe"
            ),
        ),
    ]
