# Generated by Django 2.2.16 on 2022-08-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("food", "0004_auto_20220806_1517"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(
                db_index=True, max_length=200, verbose_name="Название"
            ),
        ),
    ]