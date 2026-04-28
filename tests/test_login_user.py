import pytest
import requests
import allure

from config import LOGIN_URL
from helpers import generate_user_data


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.story("Успешный логин")
    @allure.title("Вход под существующим пользователем возвращает 200 и токены")
    def test_login_existing_user_success(self, new_user):
        credentials = {
            "email": new_user["email"],
            "password": new_user["password"],
        }

        with allure.step("Отправляем POST /api/auth/login с корректными данными"):
            response = requests.post(LOGIN_URL, json=credentials)

        with allure.step("Проверяем статус-код 200"):
            assert response.status_code == 200

        with allure.step("Проверяем success=true в теле ответа"):
            body = response.json()
            assert body["success"] is True

        with allure.step("Проверяем наличие accessToken и refreshToken"):
            assert "accessToken" in body
            assert "refreshToken" in body

        with allure.step("Проверяем email пользователя в ответе"):
            assert body["user"]["email"] == new_user["email"]

    @allure.story("Неуспешный логин")
    @allure.title("Вход с неверным паролем возвращает 401")
    def test_login_with_wrong_password_returns_401(self, new_user):
        credentials = {
            "email": new_user["email"],
            "password": "totally_wrong_password_12345",
        }

        with allure.step("Отправляем POST /api/auth/login с неверным паролем"):
            response = requests.post(LOGIN_URL, json=credentials)

        with allure.step("Проверяем статус-код 401"):
            assert response.status_code == 401

        with allure.step("Проверяем success=false и сообщение об ошибке"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "email or password are incorrect"

    @allure.story("Неуспешный логин")
    @allure.title("Вход с неверным email возвращает 401")
    def test_login_with_wrong_email_returns_401(self, new_user):
        credentials = {
            "email": "nonexistent_user_xyz@example.com",
            "password": new_user["password"],
        }

        with allure.step("Отправляем POST /api/auth/login с несуществующим email"):
            response = requests.post(LOGIN_URL, json=credentials)

        with allure.step("Проверяем статус-код 401"):
            assert response.status_code == 401

        with allure.step("Проверяем success=false и сообщение об ошибке"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "email or password are incorrect"

    @allure.story("Неуспешный логин")
    @allure.title("Вход с неверным логином и паролем возвращает 401")
    def test_login_with_wrong_credentials_returns_401(self):
        credentials = {
            "email": "completely_wrong@example.com",
            "password": "completely_wrong_password",
        }

        with allure.step("Отправляем POST /api/auth/login с полностью неверными данными"):
            response = requests.post(LOGIN_URL, json=credentials)

        with allure.step("Проверяем статус-код 401"):
            assert response.status_code == 401

        with allure.step("Проверяем success=false"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "email or password are incorrect"
