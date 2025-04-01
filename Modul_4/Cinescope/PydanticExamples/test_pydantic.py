# # CinescopeFork\Modul_4\PydanticExamples\test_pydantic.py
# from pydantic import BaseModel
# from venv import logger
#
# class User(BaseModel):  # Создается класс User с помощью BaseModel от pydantic и указывается
#     name: str       # что имя должно быть строкой
#     age: int        # возраст должен быть числом
#     adult: bool     # поле совершенолетие должно быть булевым значением
#
#
# def get_user():     # функция get_user возвращает объект dict со следующими полями
#     return {
#         "name": "Alice",
#         "age": 25,
#         "adult": "true"
#         }
#
# def test_user_data():
#     user = User(**get_user())       # Проверяем возможность конвертации данных и соответствия типов данных с помощью Pydantic
#     assert user.name == "Alice"     # Возможность дополнительных проверок
#     logger.info(f"{user.name=} {user.age=} {user.adult=}")      # а также возможность удобного взаимодействия
#     print(user)
"""
В этом коде мы используем библиотеку Pydantic для валидации и преобразования данных. Давай разберем его пошагово с точки зрения Python.

1. Определение модели данных с помощью Pydantic
from pydantic import BaseModel

class User(BaseModel):
    name: str       # Имя должно быть строкой
    age: int        # Возраст должен быть числом
    adult: bool     # Поле "совершеннолетие" должно быть булевым значением
    
### Что здесь происходит?

- `class User(BaseModel)`:
    - Мы создаем **класс** `User`, который **наследуется** от `BaseModel` из Pydantic
    - `BaseModel` автоматически добавляет функциональность проверки и преобразования данных
- Аннотация типов `name: str, age: int, adult: bool`:
    - Это говорит Python (и Pydantic), что `name` всегда должно быть строкой, `age` – целым числом, а `adult` – булевым значением (`True` или `False`).
    - **Pydantic сам конвертирует значения в нужные типы**, если это возможно!
    
### **2. Функция, которая возвращает данные в виде словаря**

```python
def get_user():
    return {
        "name": "Alice",
        "age": 25,
        "adult": "true"
    }
```
### Что здесь происходит?

- Эта функция возвращает **словарь (`dict`)** с данными пользователя.
- **Обрати внимание** на `"adult": "true"` – это строка, а не `True` (булево значение).
- По правилам `User`, `adult` должен быть `bool`, но передан **неправильный** тип данных.

💡 **Pydantic автоматически исправит это при создании объекта!**

3. Используем Pydantic для валидации и преобразования данных
def test_user_data():
    user = User(**get_user())  # Передаём данные в модель Pydantic


Что здесь происходит?

User(**get_user()) – создаём экземпляр класса User.
**get_user() – распаковываем словарь и передаём значения в User:
User(name="Alice", age=25, adult="true")

### **4. Проверяем корректность данных**

```python
    assert user.name == "Alice"
```

- Это обычный `assert`, который проверяет, что `user.name` действительно `"Alice"`.
- Если бы данные были некорректны, `Pydantic` выбросил бы ошибку **ещё при создании объекта**.


### **5. Логируем данные**

```python
    logger.info(f"{user.name=} {user.age=} {user.adult=}")
```

### Что здесь происходит?

- `f"{user.name=} {user.age=} {user.adult=}"` – это **f-строка с раскрытием переменных**.
- Выведет:
    
    ```
    user.name='Alice' user.age=25 user.adult=True
    
    ```
    
- **Демонстрирует, что Pydantic исправил "true" → `True`.**

## **Вывод: Как это работает?**

1. **Определяем модель данных** с ожидаемыми типами (`BaseModel`).
2. **Передаём словарь в Pydantic**, который **автоматически проверяет и преобразует** данные.
3. **Если что-то не так, Pydantic выбросит ошибку**.
4. **В итоге у нас чистые, проверенные данные в объекте `User`**.

### **Дополнительные примеры: ошибки и преобразования**

### **Ошибка: передаём неверный тип**

user = User(name="Alice", age="двадцать пять", adult="да")

🚫**Ошибка!**

```
pydantic_core._pydantic_core.ValidationError:
1 validation error for User
age
  Input should be a valid integer, but got str
```

**Pydantic не смог превратить `"двадцать пять"` в число и выбросил ошибку.**

✅ Pydantic сам исправляет типы, если это возможно
user = User(name="Alice", age="25", adult="true")
print(user)

Pydantic превратит "25" в 25, а "true" в True!
User(name='Alice', age=25, adult=True)

## **Почему это удобно в тестах?**

- **Не нужно вручную проверять типы** – Pydantic делает это автоматически.
- **Простая валидация API-ответов**:
    - Если запрос вернул JSON, **можно сразу преобразовать его в объект**.
- **Гарантирует, что тесты не сломаются из-за неожиданных данных**.

💡 **Вместо кучи проверок с `assert` можно просто создать Pydantic-модель и быть уверенным, что данные корректные!**

Ключевые компоненты и способы применения Pydantic
BaseModel - базовый класс для создания моделей данных. Модель описывает структуру данных и правила их валидации. 
Field -  позволяет добавлять дополнительные параметры для полей модели, такие как описание, минимальное/максимальное значение, примеры данных и тд. (https://docs.pydantic.dev/latest/concepts/fields/) Полная информация в официальной документации.
Optional  и Default -  позволяет указывать необязательные поля и значения по умолчанию.
Enum  - поддерживает Enum для ограничения возможных значений поля, а также поддерживает работу с вложенными моделями
Pydantic позволяет легко конвертировать модели в JSON и обратно.
Пример на основе класса Product отображающий основные возможности:
# CinescopeFork\Modul_4\PydanticExamples\test_pydantic.py
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from venv import logger

class ProductType(str, Enum): 
    NEW = "new"
    PREVIOUS_USE = "previous_use"

class Manufacturer(BaseModel):
    name: str
    city: Optional[str] = None
    street: Optional[str] = None
    
class Product(BaseModel):
		# поле name может иметь длину в диапазоне от 3 до 50 символов и является строкой
    name: str = Field(..., min_length=3, max_length=50, description="Название продукта")
    # поле price должно быть больше 0
    price: float = Field(..., gt=0, description="Цена продукта")
    # поле in_stock принимает булево значение и установится по умолчанию = False
    in_stock: bool = Field(default=False, description="Есть ли в наличии")
    # поле colorдолжно быть строкой и принимает значение "black" по умолчанию
    color: str = "black"  
    # поле year не обязательное. можно не указывать при создании обьекта
    year: Optional[int] = None
    # поле product принимает тип Enum (может содержать только 1 из его значений)
    product: ProductType
    # поле manufacturer принимает тип другой BaseModel
    manufacturer: Manufacturer

def test_product():
    # Пример создания обьекта + в поле price передаём строку вместо числа
    product = Product(name="Laptop", price="999.99", product=ProductType.NEW, manufacturer=Manufacturer(name="MSI"))
    logger.info(f"{product=}")
    # Output: product=Product(name='Laptop', price=999.99, in_stock=False, color='black', year=None, product=<ProductType.NEW: 'new'>, manufacturer=Manufacturer(name='MSI', city=None, street=None))

    # Пример конвертации обьекта в json
    json_data = product.model_dump_json(exclude_unset=True)
    logger.info(f"{json_data=}")
    # Output: json_data='{"name":"Laptop","price":999.99,"product":"new","manufacturer":{"name":"MSI"}}'

    # Пример конвертации json в обьект
    new_product = Product.model_validate_json(json_data)
    logger.info(f"{new_product=}")
    # Output: new_product=Product(name='Laptop', price=999.99, in_stock=False, color='black', year=None, product=<ProductType.NEW: 'new'>, manufacturer=Manufacturer(name='MSI', city=None, street=None))

Pydantic автоматически конвертирует данные в нужные типы, если это возможно.
# В поле price передаём строку вместо числа
product = Product(name="Laptop", price="999.99", product=ProductType.NEW, manufacturer=Manufacturer(name="MSI"))

Подробное объяснение ключевых компонентов Pydantic
В этом разделе мы рассмотрим ключевые механизмы Pydantic и как они помогают при работе с данными. 
Pydantic обеспечивает валидацию, преобразование и структурирование данных, что делает код более чистым, надежным и удобным в тестировании.

1. BaseModel — основа всех моделей в Pydantic
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    
**Что делает `BaseModel`?**

- **Автоматически валидирует данные** при создании объекта.
- **Конвертирует типы** (например, `"999.99"` → `999.99`).
- **Позволяет сериализовать и десериализовать** данные (например, в JSON).

Пример использования:
product = Product(name="Laptop", price="999.99")
print(product)
# Product(name='Laptop', price=999.99)

- **Pydantic автоматически преобразовал строку `"999.99"` в `float`!**
- Если бы вместо цены передали `"сто долларов"`, **Pydantic выбросил бы ошибку**.

### **2. `Field` — настройка полей**

💡`Field` позволяет задавать **ограничения и описания** для полей.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Название продукта")
    price: float = Field(..., gt=0, description="Цена продукта")

```
❓**Что здесь происходит?**

- `min_length=3, max_length=50` — имя продукта должно быть от 3 до 50 символов.
- `gt=0` — цена должна быть **больше 0**.
- `description="..."` — описание, которое будет в **JSON Schema**.

### Эллипсис или `…`

В Pydantic символ **`...`** (эллипсис) используется как значение по умолчанию для обязательных полей. Это специальный объект в Python, который в контексте Pydantic указывает, что поле **должно быть обязательно заполнено** при создании экземпляра модели

### **Разберем подробнее:**

1. **Что означает `...`?**
    - **`...`** — это сокращение для объекта **`Ellipsis`**, который является встроенным объектом в Python
    - В Pydantic он используется для обозначения того, что поле является **обязательным** (т.е. его значение должно быть предоставлено при создании экземпляра модели)
2. **Зачем использовать `...` вместо значения по умолчанию?**
    - Если вы хотите, чтобы поле было обязательным, но не хотите задавать для него значение по умолчанию, вы используете **`...`**.
    - Например:Здесь **`name`** — обязательное поле, и при создании экземпляра модели **`Product`** вы должны предоставить значение для **`name`**
        
        ```python
        name: str = Field(..., min_length=3)
        ```
        
3. **Как это работает?**
    - Когда Pydantic видит **`...`** в качестве значения по умолчанию, он проверяет, что значение для этого поля было явно передано при создании экземпляра модели
    - Если значение не передано, Pydantic вызывает ошибку валидации
4. **Пример использования:**
    
    ```python
    from pydantic import BaseModel, Field
    
    class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Название продукта")
    price: float = Field(..., gt=0, description="Цена продукта")
    
    # Попытка создать экземпляр без обязательных полей вызовет ошибку
    try:
    product = Product()
    except Exception as e:
    print(e)  # Output: "field required" для обоих полей
    
    # Корректное создание экземпляра
    product = Product(name="Laptop", price=1000.0)
    
    print(product)
    
    # Output: name='Laptop' price=1000.0
    ```
    
5. **Альтернатива `...`:**
    - Если надо сделать поле необязательным, можно использовать значение по умолчанию, например:
        
        Здесь поле **`name`** будет необязательным, и если значение не передано, оно примет значение **`"Unknown"`**
        
        ```python
        name: str = Field(default="Unknown", min_length=3)
        ```
        
6. **Почему не просто `None`?**
    - Использование **`None`** в качестве значения по умолчанию делает поле необязательным, но позволяет ему принимать значение **`None`**. Если нужно, чтобы поле было обязательным, но не имело значения по умолчанию, **`...`** — это правильный выбор

### **Пример с необязательным полем:**

```python
class Product(BaseModel):
name: str = Field(..., min_length=3)  # Обязательное поле
price: float = Field(default=0.0, ge=0)  # Необязательное поле с дефолтным значением
```

### **Подытожим:**

- **`...`** используется для обозначения обязательных полей в Pydantic
- Если поле необязательное, можно использовать значение по умолчанию (например, **`None`** или другое значение)

### **3. `Optional` и `Default` — необязательные поля**
💡

Если поле **может отсутствовать**, используем **`Optional`**.


```python
from typing import Optional

class Product(BaseModel):
    name: str
    year: Optional[int] = None  # Год выпуска не обязателен
```

- **Пример использования:**
    
    ```python
    p1 = Product(name="Phone")
    p2 = Product(name="Phone", year=2022)
    
    ```
     ➖
    
    - **`p1` создастся без `year`, потому что у него `None` по умолчанию.**
    - **`p2` создастся с `year=2022`.**
   
### **4. `Enum` — ограничение значений**

💡`Enum` помогает **ограничивать значения поля**.

```python
from enum import Enum

class ProductType(str, Enum):
    NEW = "new"
    USED = "used"
```

- **Применение в модели:**
    
    ```python
    class Product(BaseModel):
        name: str
        product_type: ProductType
    ```
💡  **Теперь `product_type` может быть ТОЛЬКО `"new"` или `"used"`.**

### **5. Вложенные модели**

<aside>
💡

Можно использовать **другие модели** как типы полей.

</aside>

```python
class Manufacturer(BaseModel):
    name: str
    city: Optional[str] = None

class Product(BaseModel):
    name: str
    manufacturer: Manufacturer  # 👈 Вложенная модель

```

- **Пример использования :**
    
    ```python
    product = Product(name="Phone", manufacturer={"name": "Samsung"})
    print(product)
    # Product(name='Phone', manufacturer=Manufacturer(name='Samsung', city=None))
    
    ```
    
    <aside>
    💡
    
    **Pydantic автоматически создал `Manufacturer` из словаря!**

### **6. Конвертация в JSON**

<aside>
💡

Pydantic умеет **превращать объекты в JSON**.

</aside>

```python
product = Product(name="Laptop", price=999.99)
json_data = product.model_dump_json(exclude_unset=True)
print(json_data)
# '{"name": "Laptop", "price": 999.99}'
```

<aside>
❓

**Что делает `model_dump_json(exclude_unset=True)`?**

- **Превращает объект в строку JSON**.
- **Пропускает поля со значением `None`** (чтобы JSON был компактным).

### **7. Обратное преобразование (из JSON в объект)**

<aside>
💡

Можно загрузить объект **из JSON**.

</aside>

```python
new_product = Product.model_validate_json(json_data)
print(new_product)
# Product(name='Laptop', price=999.99)

```

➖

**Pydantic сам разберет JSON и создаст объект.**

### **8. Автоматическая валидация данных**

<aside>
💡

**Pydantic сам проверит все поля.**

</aside>

```python
try:
    p = Product(name="TV", price="бесплатно")
except Exception as e:
    print(e)

```

<aside>
🚫

**Ошибка! `"бесплатно"` нельзя преобразовать в число.**

</aside>
"""
import json

import pytest
# CinescopeFork\Modul_4\PydanticExamples\test_pydantic.py
from pydantic import BaseModel, Field, field_validator
from venv import logger
from typing import List, Optional
from ..enums.roles import Roles
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelForTestUser(BaseModel): # Создается класс ModelForTestUser с помощью BaseModel от pydantic и указывается
    email: str     # Валидация email-адреса
    fullName: str = Field(..., min_length=1)        # Имя не должно быть пустым
    password: str = Field(..., min_length=8, max_length=20)         # Пароль: минимум 8, максимум 20 символов
    passwordRepeat: str = Field(..., min_length=8, max_length=20)   # Пароль: минимум 8, максимум 20 символов
    roles: List[Roles]   # Список ролей (например, ["USER"])
    banned: Optional[bool] = False
    verified: Optional[bool] = True

    @field_validator("email")
    def check_email(value :str) -> str:
        if "@" not in value:
            raise ValueError("email должен содержать @")
        return value

    @field_validator("password")
    def check_password(value :str) -> str:
        if len(value) < 8:
            raise ValueError("пароль должен быть минимум 8 символов")
        return value


class TestModelForTestUser:

    def test_validate_test_user(self, test_user):
        """Проверяет, что данные из фикстуры test_user валидируются через модель ModelForTestUser."""
        user = ModelForTestUser(**test_user)

        assert user.email == test_user["email"], f"email адреса не совпадают"
        assert user.fullName == test_user["fullName"], f"fullName не совпадает"
        assert user.password == test_user["password"], f"password не совпадает"
        assert user.passwordRepeat == test_user["passwordRepeat"], f"passwordRepeat не равен password"
        assert user.roles == [Roles.USER], f"Роль не совпадает"
        assert user.banned == False, f"При создании  banned = True"
        assert user.verified == True, f"При создании  verified == False"


    def test_validate_creation_user_data(self, creation_user_data):
        """Проверяет, что данные из фикстуры creation_user_data валидируются через модель ModelForTestUser."""
        user = ModelForTestUser(**creation_user_data)

        assert user.email == creation_user_data["email"], f"email адреса не совпадают"
        assert user.fullName == creation_user_data["fullName"], f"fullName не совпадает"
        assert user.password == creation_user_data["password"], f"password не совпадает"
        assert user.passwordRepeat == creation_user_data["passwordRepeat"], f"passwordRepeat не равен password"
        assert user.roles == [Roles.USER], f"Роль не совпадает"
        assert user.banned == False, f"При создании  banned = True"
        assert user.verified == True, f"При создании  verified == False"

    def test_json_serialization(self, test_user, creation_user_data):
        """Проверяет сериализацию и десериализацю через модель ModelForTestUser."""
        user1 = ModelForTestUser(**test_user)
        user2 = ModelForTestUser(**creation_user_data)

        user1_json = user1.json(exclude_unset=True)
        user2_json = user2.json()

        user1_dict = json.loads(user1_json)
        user2_dict = json.loads(user2_json)

        logger.info(f"JSON for test_user (exclude_unset=True): {user1_json}")
        logger.info(f"JSON for creation_user_data: {user2_json}")

        assert "banned" not in user1_dict, f"banned присутствует в сериализированном словаре"
        assert "verified" not in user1_dict, f"verified присутствует в сериализированном словаре"

        assert "banned" in user2_dict, f"banned отсутствует в десериализированном словаре"
        assert user2_dict["banned"] == False, f"banned = True, хотя по умолчанию должно быть False"
        assert "verified" in user2_dict, f"verified отсутствует в десериализированном словаре"
        assert user2_dict["verified"] == True, f"verified = False, хотя по умолчанию должно быть True"

    def test_invalid_email_no_at(self):

        invalid_data = {
            "email": "userexample.com",
            "fullName": "John Doe",
            "password": "Pass123!",
            "passwordRepeat": "Pass123!",
            "roles": ["USER"]
        }
        with pytest.raises(ValueError, match="email должен содержать @"):
            example = ModelForTestUser(**invalid_data)
