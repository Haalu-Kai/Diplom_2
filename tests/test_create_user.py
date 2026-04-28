import pytest
import requests
import allure

from config import REGISTER_URL
from helpers import generate_user_data


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.story("Успешное создание пользователя")
    @allure.title("Создание уникального пользователя возвращает 200 и success=true")
    def test_create_unique_user_success(self):
        user_data = generate_user_data()
        access_token = None

        with allure.step("Отправляем POST /api/auth/register с уникальными данными"):
            response = requests.post(REGISTER_URL, json=user_data)

        with allure.step("Проверяем статус-код 200"):
            assert response.status_code == 200

        with allure.step("Проверяем success=true в теле ответа"):
            body = response.json()
            assert body["success"] is True

        with allure.step("Проверяем наличие accessToken и refreshToken"):
            assert "accessToken" in body
            assert "refreshToken" in body
            access_token = body["accessToken"]

        with allure.step("Проверяем данные пользователя в ответе"):
            assert body["user"]["email"] == user_data["email"]
            assert body["user"]["name"] == user_data["name"]

        # Teardown
        if access_token:
            requests.delete(
                REGISTER_URL.replace("/register", "/user"),
                headers={"Authorization": access_token}
            )

    @allure.story("Регистрация уже существующего пользователя")
    @allure.title("Повторная регистрация существующего пользователя возвращает 403")
    def test_create_already_registered_user_returns_403(self, new_user):
        duplicate_data = {
            "email": new_user["email"],
            "password": new_user["password"],
            "name": new_user["name"],
        }

        with allure.step("Отправляем POST /api/auth/register с уже существующим email"):
            response = requests.post(REGISTER_URL, json=duplicate_data)

        with allure.step("Проверяем статус-код 403"):
            assert response.status_code == 403

        with allure.step("Проверяем success=false и сообщение об ошибке"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "User already exists"

    @allure.story("Создание пользователя без обязательного поля")
    @allure.title("Регистрация без поля email возвращает 403")
    def test_create_user_without_email_returns_403(self):
        user_data = generate_user_data()
        del user_data["email"]

        with allure.step("Отправляем POST /api/auth/register без поля email"):
            response = requests.post(REGISTER_URL, json=user_data)

        with allure.step("Проверяем статус-код 403"):
            assert response.status_code == 403

        with allure.step("Проверяем success=false и сообщение об ошибке"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "Email, password and name are required fields"

    @allure.story("Создание пользователя без обязательного поля")
    @allure.title("Регистрация без поля password возвращает 403")
    def test_create_user_without_password_returns_403(self):
        user_data = generate_user_data()
        del user_data["password"]

        with allure.step("Отправляем POST /api/auth/register без поля password"):
            response = requests.post(REGISTER_URL, json=user_data)

        with allure.step("Проверяем статус-код 403"):
            assert response.status_code == 403

        with allure.step("Проверяем success=false и сообщение об ошибке"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "Email, password and name are required fields"

    @allure.story("Создание пользователя без обязательного поля")
    @allure.title("Регистрация без поля name возвращает 403")
    def test_create_user_without_name_returns_403(self):
        user_data = generate_user_data()
        del user_data["name"]

        with allure.step("Отправляем POST /api/auth/register без поля name"):
            response = requests.post(REGISTER_URL, json=user_data)

        with allure.step("Проверяем статус-код 403"):
            assert response.status_code == 403

        with allure.step("Проверяем success=false и сообщение об ошибке"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "Email, password and name are required fields"
