# Generated by Django 2.2.16 on 2022-08-08 17:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("food", "0006_auto_20220808_1417"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="tag",
            field=models.ManyToManyField(
                related_name="recipes", to="food.Tag", verbose_name="Тег"
            ),
        ),
    ]