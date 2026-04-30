import pytest
import requests
import allure

from config import ORDERS_URL, MSG_NO_INGREDIENTS


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Авторизованный заказ")
    @allure.title("Создание заказа с авторизацией и ингредиентами возвращает 200")
    def test_create_order_with_auth_and_ingredients(self, new_user, valid_ingredients):
        headers = {"Authorization": new_user["accessToken"]}
        payload = {"ingredients": valid_ingredients}

        with allure.step("Отправляем POST /api/orders с авторизацией и ингредиентами"):
            response = requests.post(ORDERS_URL, json=payload, headers=headers)

        with allure.step("Проверяем статус-код 200"):
            assert response.status_code == 200

        with allure.step("Проверяем success=true"):
            body = response.json()
            assert body["success"] is True

        with allure.step("Проверяем наличие номера заказа"):
            assert "order" in body
            assert body["order"]["number"] > 0

    @allure.story("Неавторизованный заказ")
    @allure.title("Создание заказа без авторизации возвращает 200 (анонимный заказ)")
    def test_create_order_without_auth(self, valid_ingredients):
        payload = {"ingredients": valid_ingredients}

        with allure.step("Отправляем POST /api/orders без заголовка авторизации"):
            response = requests.post(ORDERS_URL, json=payload)

        with allure.step("Проверяем статус-код 200"):
            assert response.status_code == 200

        with allure.step("Проверяем success=true (анонимный заказ принимается)"):
            body = response.json()
            assert body["success"] is True

        with allure.step("Проверяем наличие номера заказа"):
            assert "order" in body
            assert body["order"]["number"] > 0

    @allure.story("Заказ с ингредиентами")
    @allure.title("Создание заказа с валидными ингредиентами возвращает номер заказа")
    def test_create_order_with_ingredients_returns_order_number(self, new_user, valid_ingredients):
        headers = {"Authorization": new_user["accessToken"]}
        payload = {"ingredients": valid_ingredients}

        with allure.step("Отправляем POST /api/orders с ингредиентами"):
            response = requests.post(ORDERS_URL, json=payload, headers=headers)

        with allure.step("Проверяем, что в ответе есть числовой номер заказа"):
            body = response.json()
            assert isinstance(body["order"]["number"], int)

    @allure.story("Заказ без ингредиентов")
    @allure.title("Создание заказа без ингредиентов возвращает 400")
    def test_create_order_without_ingredients_returns_400(self, new_user):
        headers = {"Authorization": new_user["accessToken"]}
        payload = {"ingredients": []}

        with allure.step("Отправляем POST /api/orders с пустым списком ингредиентов"):
            response = requests.post(ORDERS_URL, json=payload, headers=headers)

        with allure.step("Проверяем статус-код 400"):
            assert response.status_code == 400

        with allure.step("Проверяем success=false и сообщение об ошибке"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == MSG_NO_INGREDIENTS

    @allure.story("Заказ с неверным хешем ингредиентов")
    @allure.title("Создание заказа с невалидным хешем ингредиента возвращает 500")
    def test_create_order_with_invalid_ingredient_hash_returns_500(self, new_user):
        headers = {"Authorization": new_user["accessToken"]}
        payload = {"ingredients": ["invalid_hash_000", "bad_id_111"]}

        with allure.step("Отправляем POST /api/orders с невалидными хешами ингредиентов"):
            response = requests.post(ORDERS_URL, json=payload, headers=headers)

        with allure.step("Проверяем статус-код 500"):
            assert response.status_code == 500

    @allure.story("Заказ без ингредиентов")
    @allure.title("Создание заказа без авторизации и без ингредиентов возвращает 400")
    def test_create_order_no_auth_no_ingredients_returns_400(self):
        payload = {"ingredients": []}

        with allure.step("Отправляем POST /api/orders без авторизации и без ингредиентов"):
            response = requests.post(ORDERS_URL, json=payload)

        with allure.step("Проверяем статус-код 400"):
            assert response.status_code == 400

        with allure.step("Проверяем success=false"):
            body = response.json()
            assert body["success"] is False
