# Generated by Django 2.2.16 on 2022-08-06 10:21

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
        ("food", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all "
                        "permissions without explicitly assigning "
                        "them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already "
                            "exists. "
                        },
                        help_text="Required. 150 characters or fewer. "
                        "Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into "
                        "this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be "
                        "treated as active. Unselect this instead "
                        "of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("user", "пользователь"),
                            ("admin", "администратор"),
                        ],
                        default="user",
                        max_length=25,
                        verbose_name="Роль пользователя",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=150, verbose_name="Пароль"),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="Фамилия"),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="Email"),
                ),
                (
                    "cart",
                    models.ManyToManyField(
                        related_name="users_added_to_cart",
                        to="food.Recipe",
                        verbose_name="Находится ли в корзине",
                    ),
                ),
                (
                    "favorite",
                    models.ManyToManyField(
                        related_name="users_favorited",
                        to="food.Recipe",
                        verbose_name="Находится ли в избранном",
                    ),
                ),
                (
                    "follower",
                    models.ManyToManyField(
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Подписчик",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user "
                        "will get all permissions granted to each "
                        "of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]