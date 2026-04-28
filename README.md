# Stellar Burgers — API тесты (Задание 2)

## Структура проекта

```
stellar_burgers_api/
├── config.py               # URL и эндпоинты
├── helpers.py              # Генерация тестовых данных
├── conftest.py             # Фикстуры pytest (создание/удаление пользователя, ингредиенты)
├── pytest.ini              # Конфиг pytest + allure
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── test_create_user.py  # Тесты создания пользователя
    ├── test_login_user.py   # Тесты логина
    └── test_create_order.py # Тесты создания заказа
```

## Покрытые сценарии

### Создание пользователя (`POST /api/auth/register`)
- Создание уникального пользователя → 200
- Создание уже зарегистрированного пользователя → 403
- Создание без поля `email` → 403
- Создание без поля `password` → 403
- Создание без поля `name` → 403

### Логин пользователя (`POST /api/auth/login`)
- Вход под существующим пользователем → 200
- Вход с неверным паролем → 401
- Вход с неверным email → 401
- Вход с полностью неверными данными → 401

### Создание заказа (`POST /api/orders`)
- С авторизацией и ингредиентами → 200
- Без авторизации (анонимный заказ) → 200
- С ингредиентами — проверка номера заказа → 200
- Без ингредиентов (авторизованный) → 400
- С неверным хешем ингредиентов → 500
- Без авторизации и без ингредиентов → 400

## Установка и запуск

### 1. Установить зависимости
```bash
pip install -r requirements.txt
```

### 2. Запустить тесты с генерацией отчёта Allure
```bash
pytest --alluredir=allure-results
```

### 3. Открыть Allure-отчёт
```bash
allure serve allure-results
```

> Для работы команды `allure` нужно установить Allure CLI:
> - macOS: `brew install allure`
> - Windows: https://allurereport.org/docs/install-for-windows/
> - Linux: https://allurereport.org/docs/install-for-linux/

## Примечания

- Фикстура `new_user` автоматически создаёт пользователя перед тестом и удаляет после.
- Фикстура `valid_ingredients` запрашивает реальные ингредиенты из API один раз за сессию.
- Тесты требуют доступа к интернету для работы с `https://stellarburgers.education-services.ru`.
