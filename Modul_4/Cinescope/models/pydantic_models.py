# CinescopeFork\Modul_4\PydanticExamples\test_pydantic.py
from pydantic import BaseModel, EmailStr, Field
# from venv import logger
# from typing import Optional, List
# from ..enums.roles import Roles


# class ModelForTestUser(BaseModel): # Создается класс ModelForTestUser с помощью BaseModel от pydantic и указывается
#     email: EmailStr     # Валидация email-адреса
#     fullName: str = Field(..., min_length=1)        # Имя не должно быть пустым
#     password: str = Field(..., min_length=8, max_length=20)         # Пароль: минимум 8, максимум 20 символов
#     passwordRepeat: str = Field(..., min_length=8, max_length=20)   # Пароль: минимум 8, максимум 20 символов
#     roles: List[Roles]   # Список ролей (например, ["USER"])
#     banned: Optional[bool] = False
#     verified: Optional[bool] = True

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

# Создаем объект
product = Product(name="Book", price=199.99, in_stock=True)

# Сериализиация (Python → JSON)
json_data = product.model_dump_json()
print(json_data)

# Десериализиация (JSON → Python)
new_product = Product.model_validate_json(json_data)
print(new_product)
