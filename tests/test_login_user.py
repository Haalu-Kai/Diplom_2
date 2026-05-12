import pytest
import requests
import allure

from config import LOGIN_URL, MSG_WRONG_CREDENTIALS


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
    @allure.title("Вход с неверным логином и/или паролем возвращает 401")
    @pytest.mark.parametrize("email_override, password_override", [
        ("totally_wrong@example.com", None),           
        (None, "totally_wrong_password_12345"),          
        ("completely_wrong@example.com", "wrong_pass"), 
    ])
    def test_login_with_wrong_credentials_returns_401(
        self, new_user, email_override, password_override
    ):
        credentials = {
            "email": email_override if email_override else new_user["email"],
            "password": password_override if password_override else new_user["password"],
        }

        with allure.step(f"Отправляем POST /api/auth/login: email={credentials['email']}"):
            response = requests.post(LOGIN_URL, json=credentials)

        with allure.step("Проверяем статус-код 401"):
            assert response.status_code == 401

        with allure.step("Проверяем success=false и сообщение об ошибке"):
            body = response.json()
            assert body["success"] is False
            assert body["message"] == MSG_WRONG_CREDENTIALS
