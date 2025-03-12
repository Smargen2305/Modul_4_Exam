# import pytest
# import requests
# from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT
from ....Cinescope.api.api_manager import ApiManager

class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user).json()

        # Проверки
        assert response["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response, "ID пользователя отсутствует в ответе"
        assert "roles" in response, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data).json()

        # Проверки
        assert "accessToken" in response, "Токен доступа отсутствует в ответе"
        assert response["user"]["email"] == registered_user["email"], "Email не совпадает"