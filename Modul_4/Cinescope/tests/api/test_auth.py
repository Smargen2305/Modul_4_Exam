import datetime
# from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT
from ....Cinescope.api.api_manager import ApiManager
from ...enums.roles import Roles
from pydantic import Field, BaseModel, field_validator
from typing import List, Optional
from ...conftest import registered_user

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")
    id: Optional[str] = None

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError ("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

class LoginUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    roles: List[str]
    id: Optional[str] = None


class TestAuthAPI:
    def test_register_user(self, api_manager, registered_user):
        """
        Тест на регистрацию пользователя.
        """
        # Проверяем, что пользователь успешно зарегистрирован
        assert registered_user.id is not None, "ID пользователя должен быть установлен после регистрации"
        assert registered_user.email, "Email пользователя должен быть установлен"

        # # Преобразуем roles перед отправкой
        # user_data = registered_user.model_dump()
        # user_data["roles"] = [role.value for role in user_data["roles"]]
        #
        # response = api_manager.auth_api.register_user(user_data=user_data, expected_status=201)
        # register_user_response = RegisterUserResponse(**response.json())
        #
        # # Проверки
        # assert register_user_response.email == registered_user.email, "Email не совпадает"

    def test_register_and_login_user(self, api_manager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }
        # Отправляем запрос на авторизацию
        response = api_manager.auth_api.login_user(login_data=login_data, expected_status=200)
        response_json = response.json()

        # Извлекаем данные пользователя из ответа
        reg_login_user_response = LoginUserResponse(**response_json["user"])

        # Проверяем наличие токена и одну проверку на email
        assert "accessToken" in response_json, "Токен доступа отсутствует в ответе"
        assert reg_login_user_response.email == registered_user.email, f"Ожидался email {registered_user.email}, но получен {reg_login_user_response.email}"