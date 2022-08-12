import json
import os
from http import HTTPStatus

from django.test import TestCase
from food.models import Ingredient, Recipe, Tag
from rest_framework.test import APIClient
from users.models import User


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
        )
        data_dir = os.path.join(base_dir, "data")
        path_to_json_file = f"{data_dir}/test_endpoints.json"
        json_file = open(path_to_json_file)
        json_data = json.load(json_file)
        json_file.close()

        cls.endpoints_dict = {
            "guest": {
                HTTPStatus.OK: json_data["GUEST"],
                HTTPStatus.UNAUTHORIZED: json_data["USER"],
                HTTPStatus.NOT_FOUND: json_data["NON_EXISTING"],
            },
            "user": {
                HTTPStatus.OK: json_data["USER"],
                HTTPStatus.NOT_FOUND: json_data["NON_EXISTING"],
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
