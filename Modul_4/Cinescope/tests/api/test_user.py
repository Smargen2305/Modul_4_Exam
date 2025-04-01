
from ...enums.roles import Roles
from pydantic import Field, BaseModel, field_validator
from typing import List, Optional

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Пароли должны совпадать")
    roles: List[Roles]
    verified: bool = True
    banned: bool = False
    id: Optional[str] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

def test_create_user(self, super_admin, creation_user_data):

    response = super_admin.api.user_api.create_user(creation_user_data).json()

    assert response.get('id') and response['id'] != '', "ID должен быть НЕ пустым"
    assert response.get('email') == creation_user_data['email']
    assert response.get('fullName') == creation_user_data['fullName']
    assert response.get('roles', []) == creation_user_data['roles']
    assert response.get('verified') is True


def test_get_user_by_locator(self, super_admin,creation_user_data):

    created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()

    response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
    response_by_email = super_admin.api.user_api.get_user(created_user_response['email']).json()

    assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
    assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
    assert response_by_id.get('email') == creation_user_data['email']
    assert response_by_id.get('fullName') == creation_user_data['fullName']
    assert response_by_id.get('roles', []) == creation_user_data['roles']
    assert response_by_id.get('verified') is True

def test_get_user_by_id_common_user(self, common_user):
    # тест, в котором запрос будет происходить от юзера с ролью USER
    # Мы будем ожидать ответ от сервера 403 forbidden
    common_user.api.user_api.get_user(common_user.email, expected_status=403)






