# Generated by Django 2.2.16 on 2022-08-12 13:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("food", "0008_auto_20220810_1804"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ("-id",),
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
            },
        ),
    ]
