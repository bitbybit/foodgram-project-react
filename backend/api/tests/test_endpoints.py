from http import HTTPStatus

from django.test import TestCase
from food.models import Ingredient, Recipe, Tag
from rest_framework.test import APIClient
from users.models import User

IMAGE_BASE64 = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD"
    "///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
    "AAggCByxOyYQAAAABJRU5ErkJggg== "
)

USER = (
    # Список пользователей
    {
        "method": "get",
        "url": "/api/users/",
    },
    # Профиль пользователя
    {
        "method": "get",
        "url": "/api/users/1/",
    },
    {
        "method": "get",
        "url": "/api/users/999/",
        "status": HTTPStatus.NOT_FOUND,
    },
    # Текущий пользователь
    {
        "method": "get",
        "url": "/api/users/me/",
    },
    # Изменение пароля
    {
        "method": "post",
        "url": "/api/users/set_password/",
        "payload": {
            "new_password": "new_password",
            "current_password": "current_password",
        },
        "status": HTTPStatus.NO_CONTENT,
    },
    # Удаление токена
    {
        "method": "post",
        "url": "/api/auth/token/logout/",
        "status": HTTPStatus.NO_CONTENT,
    },
    # Создание рецепта
    {
        "method": "post",
        "url": "/api/recipes/",
        "payload": {
            "ingredients": [{"id": 1, "amount": 2}],
            "tags": [
                1,
            ],
            "image": IMAGE_BASE64,
            "name": "Название",
            "text": "Описание",
            "cooking_time": 1,
        },
        "status": HTTPStatus.CREATED,
    },
    # Обновление рецепта
    {
        "method": "patch",
        "url": "/api/recipes/1/",
        "payload": {
            "ingredients": [{"id": 1, "amount": 2}],
            "tags": [
                1,
            ],
            "image": IMAGE_BASE64,
            "name": "Название",
            "text": "Описание",
            "cooking_time": 1,
        },
        "status": HTTPStatus.FORBIDDEN,
    },
    # Удаление рецепта
    {
        "method": "delete",
        "url": "/api/recipes/1/",
        "status": HTTPStatus.FORBIDDEN,
    },
    # Скачать список покупок
    {
        "method": "get",
        "url": "/api/recipes/download_shopping_cart/",
    },
    # Добавить рецепт в список покупок
    {
        "method": "post",
        "url": "/api/recipes/1/shopping_cart/",
        "status": HTTPStatus.CREATED,
    },
    # Удалить рецепт из списка покупок
    {
        "method": "delete",
        "url": "/api/recipes/1/shopping_cart/",
        "status": HTTPStatus.NO_CONTENT,
    },
    # Добавить рецепт в избранное
    {
        "method": "post",
        "url": "/api/recipes/1/favorite/",
        "status": HTTPStatus.CREATED,
    },
    # Удалить рецепт из избранного
    {
        "method": "delete",
        "url": "/api/recipes/1/favorite/",
        "status": HTTPStatus.NO_CONTENT,
    },
    # Мои подписки
    {
        "method": "get",
        "url": "/api/users/subscriptions/",
        "status": HTTPStatus.OK,
    },
    # Подписаться на пользователя
    {
        "method": "post",
        "url": "/api/users/2/subscribe/",
        "status": HTTPStatus.CREATED,
    },
    # Отписаться от пользователя
    {
        "method": "delete",
        "url": "/api/users/2/subscribe/",
        "status": HTTPStatus.NO_CONTENT,
    },
)

GUEST = (
    # Профиль пользователя
    {
        "method": "get",
        "url": "/api/users/999/",
        "status": HTTPStatus.UNAUTHORIZED,
    },
    # Регистрация пользователя
    {
        "method": "post",
        "url": "/api/users/",
        "payload": {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "Qwerty123",
        },
        "status": HTTPStatus.CREATED,
    },
    # Получить токен авторизации
    {
        "method": "post",
        "url": "/api/auth/token/login/",
        "payload": {
            "password": "current_password",
            "email": "test@test.com",
        },
    },
    # Список тегов
    {
        "method": "get",
        "url": "/api/tags/",
    },
    # Получение тега
    {
        "method": "get",
        "url": "/api/tags/1/",
    },
    # Список рецептов
    {
        "method": "get",
        "url": "/api/recipes/",
    },
    # Получение рецепта
    {
        "method": "get",
        "url": "/api/recipes/1/",
    },
    # Список ингредиентов
    {
        "method": "get",
        "url": "/api/ingredients/",
    },
    # Получение ингредиента
    {
        "method": "get",
        "url": "/api/ingredients/1/",
    },
)

NON_EXISTING = (
    {
        "method": "get",
        "url": "/unexisting_endpoint/",
    },
    {
        "method": "get",
        "url": "/api/tags/999/",
    },
    {
        "method": "get",
        "url": "/api/recipes/999/",
    },
    {
        "method": "get",
        "url": "/api/ingredients/999/",
    },
)


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.endpoints_dict = {
            "guest": {
                HTTPStatus.OK: GUEST,
                HTTPStatus.UNAUTHORIZED: USER,
                HTTPStatus.NOT_FOUND: NON_EXISTING,
            },
            "user": {
                HTTPStatus.OK: USER,
                HTTPStatus.NOT_FOUND: NON_EXISTING,
            },
        }

        cls.user = User.objects.create(
            username="test",
            email="test@test.com",
        )
        cls.user.set_password("current_password")
        cls.user.save()

        author = User.objects.create(username="author")

        tag = Tag.objects.create(
            name="Завтрак",
            color="#E26C2D",
            slug="breakfast",
        )

        ingredient = Ingredient.objects.create(
            name="Капуста",
            measurement_unit="кг",
        )

        recipe = Recipe.objects.create(
            author=author,
            name="Название",
            image=IMAGE_BASE64,
            text="Описание",
            cooking_time=60,
        )
        recipe.tag.add(tag)
        recipe.ingredient.add(
            ingredient,
            through_defaults={"amount": 2},
        )
        recipe.save()

    def setUp(self):
        self.guest_client = APIClient()

        self.user_client = APIClient()
        self.user_client.force_authenticate(user=URLTests.user)

    def test_endpoints_http_code(self):
        """
        Проверка ожидаемого кода ответа.
        """
        if not hasattr(self, "endpoints_dict"):
            return

        for user_type, endpoints in self.endpoints_dict.items():
            for http_code_expected, endpoint in endpoints.items():
                for data in endpoint:
                    client = getattr(self, f"{user_type}_client")

                    payload = {}
                    if data.get("payload"):
                        payload = data.get("payload")

                    response = getattr(client, data.get("method"))(
                        data.get("url"),
                        data=payload,
                        format="json",
                    )

                    if (
                        data.get("status")
                        and http_code_expected != HTTPStatus.UNAUTHORIZED
                    ):
                        http_code_assert = data.get("status")
                    else:
                        http_code_assert = http_code_expected

                    try:
                        content = f" - {response.content}"
                    except AttributeError:
                        content = None

                    with self.subTest(
                        f"{user_type} - {data.get('method')} {data.get('url')}"
                        f"{content}"
                    ):
                        self.assertEqual(
                            response.status_code, http_code_assert
                        )
