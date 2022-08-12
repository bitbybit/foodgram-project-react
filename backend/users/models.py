from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    ROLE_CHOICES = (
        ("user", "пользователь"),
        ("admin", "администратор"),
    )

    role = models.CharField(
        choices=ROLE_CHOICES,
        default="user",
        max_length=25,
        verbose_name="Роль пользователя",
    )
    password = models.CharField(
        max_length=150,
        verbose_name="Пароль",
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
    )
    email = models.EmailField(
        db_index=True,
        verbose_name="Email",
    )
    follower = models.ManyToManyField(
        "self",
        blank=True,
        related_name="following",
        symmetrical=False,
        verbose_name="Подписчик",
    )
    favorite = models.ManyToManyField(
        "food.Recipe",
        blank=True,
        related_name="users_favorited",
        verbose_name="Находится ли в избранном",
    )
    cart = models.ManyToManyField(
        "food.Recipe",
        blank=True,
        related_name="users_added_to_cart",
        verbose_name="Находится ли в корзине",
    )
