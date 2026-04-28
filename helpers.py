import random
import string


def generate_random_string(length=10):
    """Генерирует случайную строку из букв нижнего регистра."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_user_data():
    """Генерирует данные нового пользователя."""
    suffix = generate_random_string(8)
    return {
        "email": f"test_{suffix}@example.com",
        "password": f"password_{suffix}",
        "name": f"User_{suffix}"
    }
