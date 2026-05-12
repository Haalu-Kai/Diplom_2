import pytest
import requests
import allure

from config import REGISTER_URL, LOGIN_URL, INGREDIENTS_URL
from helpers import generate_user_data


@pytest.fixture(scope="function")
def new_user():
    """
    Создаёт нового пользователя перед тестом и удаляет его после.
    Возвращает словарь с данными пользователя и токеном.
    """
    user_data = generate_user_data()

    response = requests.post(REGISTER_URL, json=user_data)
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"

    body = response.json()
    access_token = body.get("accessToken")

    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "accessToken": access_token,
    }

    # Teardown: удаляем пользователя
    if access_token:
        requests.delete(
            f"{REGISTER_URL.replace('/register', '/user')}",
            headers={"Authorization": access_token}
        )


@pytest.fixture(scope="session")
def valid_ingredients():
    """
    Получает реальные хеши ингредиентов из API один раз за сессию.
    Возвращает список из двух id ингредиентов.
    """
    response = requests.get(INGREDIENTS_URL)
    assert response.status_code == 200, "Не удалось получить ингредиенты"
    ingredients = response.json()["data"]
    assert len(ingredients) >= 2, "Недостаточно ингредиентов в API"
    return [ingredients[0]["_id"], ingredients[1]["_id"]]
