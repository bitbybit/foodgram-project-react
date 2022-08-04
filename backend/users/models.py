from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "пользователь"),
        ("admin", "администратор"),
    )

    role = models.CharField(
        max_length=25,
        verbose_name="Роль пользователя",
        choices=ROLE_CHOICES,
        default="user",
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=150,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
    )
    email = models.EmailField(
        verbose_name="Email",
    )
