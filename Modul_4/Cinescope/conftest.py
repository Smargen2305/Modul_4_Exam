from faker import Faker
import pytest
import requests
from .constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, MOVIE_ENDPOINT
from .custom_requester.custom_requester import CustomRequester
from .tests.api.test_user import TestUser
from .utils.data_generator import DataGenerator
from .api.auth_api import AuthAPI
from .api.api_manager import ApiManager
from .resources.user_creds import SuperAdminCreds
from .entities.user import User
from .enums.roles import Roles

faker = Faker()

@pytest.fixture(scope="function")
def test_user() -> TestUser:
    """
    Генерация случайного пользователя для тестов.
    """
    # random_email = DataGenerator.generate_random_email()
    # random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()
    #
    # return {
    #     "email": random_email,
    #     "fullName": random_name,
    #     "password": random_password,
    #     "passwordRepeat": random_password,  # Убедимся, что password и passwordRepeat совпадают
    #     "roles": [Roles.USER.value]
    # }
    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    # Получаем данные из test_user
    user_data = test_user.model_dump()

    # Преобразуем roles в список строк
    user_data["roles"] = [role.value for role in user_data["roles"]]

    # Регистрируем пользователя
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=user_data,
        expected_status=201
    )
    response_data = response.json()
    # Обновляем данные пользователя (включаем ID из ответа регистрации)
    # Создаем копию test_user и добавляем id
    registered_user = test_user.model_copy(update={"id": response_data["id"]})
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

#
# @pytest.fixture(scope="session")
# def auth_api(requester):
#     """
#     Фикстура для работы с AuthAPI.
#     """
#     return AuthAPI(session=requester)

# @pytest.fixture(scope="session")
# def user_api(requester):
#     """
#     Фикстура для работы с UserAPI.
#     """
#     return UserAPI(session=requester)

@pytest.fixture(scope="function")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="function")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture(scope="session")
def super_admin_token(api_manager):
    """
    Фикстура для получения токена авторизации SUPER_ADMIN.
    :param api_manager: Экземпляр ApiManager.
    :return: Токен авторизации.
    """
    login_data = {
        "email": SuperAdminCreds.USERNAME,
        "password": SuperAdminCreds.PASSWORD
    }
    response = api_manager.auth_api.login_user(login_data)
    return response.json()["accessToken"]

@pytest.fixture(scope="function")
def movie_data():
    """
        Фикстура для создания тестовых данных фильма.
        :return: Словарь с данными фильма.
    """
    return {
        "name": DataGenerator.generate_random_movie_name(), # генератор
        "imageUrl": "https://image.url",
        "price": DataGenerator.generate_random_movie_price(),       # генератор
        "description": DataGenerator.generate_random_movie_description(), # генератор
        "location": DataGenerator.generate_random_location(), # генератор списка
        "published": True,
        "genreId": 1
    }

# @pytest.fixture
# def create_movie(api_manager, movie_data, super_admin_token):
#     """
#     Фикстура для создания фильма и получения его данных.
#     :param api_manager: Экземпляр ApiManager.
#     :param movie_data: Данные фильма.
#     :param super_admin_token: Токен авторизации SUPER_ADMIN.
#     :return: Словарь с данными созданного фильма, включая ID.
#     """
#     response = api_manager.films_api.create_movie(movie_data, super_admin_token)
#     response_data = response.json()
#     created_movie = movie_data.copy()
#     created_movie["id"] = response_data["id"]
#     yield created_movie
#     # Очистка: удаляем фильм после теста
#     api_manager.films_api.delete_movie(created_movie["id"], super_admin_token)

## Добавим фикстуру на создание сессии юзера в conftest и доработаем ApiManager
@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

"""
1. **Создание пула сессий** (**`user_pool`**):
    Список для хранения всех созданных в тесте сессий
    
2. **Фабричная функция** (**`_create_user_session`**):
    - Создает новую сессию **`requests.Session()`**
    - Инициализирует объект **`ApiManager`** (Это мы его в последствии будем передавать юзеру)
    - Добавляет сессию в **`user_pool`** Этот список сессий нам понадобится для того, что бы после `yield` в конце теста закрыть все сессии
    
3. **Возврат фабрики** :
    Запрашиваемая фикстура или тест получают доступ к **`_create_user_session`**, чтобы создавать сессии по требованию
    
4. **Закрытие сессий** (после теста):
    Все сессии из **`user_pool`** закроются, даже если тест упал с ошибкой
    Для этого нам понадобится доработать api_manager, добавив в него метод закрытия сессии. Сделаем это!
"""

"""
Назначение фикстуры user_session()
Фикстура **`user_session()`** управляет жизненным циклом пользовательских сессий для API-тестов. Она позволяет:

- Создавать новые сессии (объекты **`requests.Session`**) для разных пользователей
- Автоматически закрывать все созданные сессии после завершения теста (Еще раз - мы созданные сессии юзера при каждом обращении к фикстуре кладем в список. А в конце - проходясь по каждой сессии в списке их закрываем!)
- Изолировать юзеров внутри теста друг от друга (каждый работает с независимыми сессиями)
"""

"""
### А что по принципам ООП? Ну тут все просто:

- **Инкапсуляция**:
    Логика создания и удаления сессий скрыта внутри фикстуры. Тесты не будут знать, как это работает — они только будут вызывать создание юзера, который в свою очередь примет в себя сессию через  **`_create_user_session()`**.
    
- **DRY (Don’t Repeat Yourself)**:
    Не нужно писать код для создания и закрытия сессий в каждом тесте — это делает фикстура
    
- **Управление ресурсами:**
    Гарантирует, что все сессии будут корректно закрыты, даже при падении теста
    
- **Гибкость** :
    Можно создать сколько угодно юзеров с разными сессиями внутри одного теста (а то и несколько сессий для 1 юзера!)
"""

# Сделаем фикстуру, которая будет создавать юзера, используя раннее написанную модель User:
@pytest.fixture(scope="function")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )
    super_admin.api.auth_api.authentication_user(super_admin.creds, expected_status=200)
    return super_admin

"""
### “Что делает?”
Фикстура super_admin создает и настраивает объект пользователя с ролью суперадминистратора , 
который используется в тестах для выполнения административных действий (например, создание других пользователей, управление ролями и тд)
Этот суперадмин нам пригодится, чтобы создавать новых юзеров или менять им роли

### На вопрос “Зачем нужна отдельная фикстура на это?” отвечаем:

- Упрощает доступ к суперадмину в тестах. Достаточно просто передать фикстуру и можно через него сразу пользоваться апишкой
- Автоматически аутентифицирует суперадмина. Тест становится более читаемым, поскольку нет вызова логинов, кред и тд.

### Как работает:

1. **Создание новой сессии** :
    - Вызывается фикстура **`user_session`**, которая создает новую сессию через **`requests.Session()`** и добавляет её в пул сессий
2. **Инициализация объекта `User`** :
    - Создается объект **`User`** с параметрами:
        - Имя пользователя (**`SuperAdminCreds.USERNAME` )**
        - Пароль (**`SuperAdminCreds.PASSWORD`**)
        - Роль (**`Roles.SUPER_ADMIN.value`**)
        - Сессия (**`new_session` ) -** по факту это уже инициализированный объект ApiManager с готовой сессией, через который мы работаем с апи
3. **Аутентификация** :
    - Вызывается метод **`authenticate()`** из **`auth_api`**, который выполняет вход суперадмина и сохраняет токен аутентификации в заголовки сессии
4. **Возврат объекта** :
    - Готовый объект **`super_admin`** возвращается в тест для использования
"""

# Напишем новую фикстуру, которая обновит дату из старой и вернет новый словарь:
@pytest.fixture(scope="function")
def creation_user_data(test_user):
    """
    Фикстура для создания данных пользователя с verified=True и banned=False.
    """
    return test_user.model_copy(update={
        "verified": True,
        "banned": False
    })

# Фикстуры для тестов под разные роли

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authentication_user(common_user.creds)
    return common_user

"""
Довольно простая фикстура, похожа на фикстуру `super_admin` , из нового тут:

1. Мы уже получаем авторизованного супер-админа, используя фикстуру `super_admin`
2. Мы создаем юзера Супер админом при помощи нового метода `create_user()`
3. После, созданный `common_user` аутентифицируется в системе, его заголовок обновляется токеном и этим юзером с ролью “юзер” мы можем пользоваться в наших тестах
"""

# Фикстура, по примеру как сделана common_user, которая будет возвращать юзера с ролью ADMIN
@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    # Копируем creation_user_data и обновляем роль на ADMIN
    admin_data = creation_user_data.copy()
    admin_data['roles'] = [Roles.ADMIN.value]       # Устанавливаем роль ADMIN

    admin_user = User(
        admin_data['email'],
        admin_data['password'],
        [Roles.ADMIN.value],
        new_session
    )
    # Создаем пользователя с ролью ADMIN
    super_admin.api.user_api.create_user(admin_data)
    # Аутентифицируем нового пользователя
    admin_user.api.auth_api.authentication_user(admin_user.creds)
    return admin_user


"""
### Параметризация

## **Что такое параметризация?**
Параметризация – это **способ автоматического повторного запуска одного и того же теста** с разными входными данными. Это позволяет:

1. **Избежать дублирования кода**
2. **Проверять один и тот же функционал с разными данными**
3. **Повысить покрытие тестов, варьируя параметры**

Вместо того чтобы писать отдельные тесты для каждой комбинации данных, мы можем использовать **`@pytest.mark.parametrize`**, чтобы передать в тест **разные значения**.


### Декоратор `@pytest.mark.parametrize`
Основным инструментом для параметризации тестов является декоратор `@pytest.mark.parametrize`. Его синтаксис:

@pytest.mark.parametrize("param_name", [value1, value2, ....])
или для нескольких параметров
@pytest.mark.parametrize("param1,param2...", [(value_1, value_2, ...), (value2_1, value2_2, ...)])

### Технические особенности работы декоратора:

1. **Первый аргумент** — строка с именами параметров (через запятую без пробелов)
2. **Второй аргумент** — список значений или список кортежей значений
3. Pytest создаст отдельный тест для каждого набора параметров
4. Параметры передаются в тестовую функцию в том же порядке, в котором они указаны в декораторе

Рассмотрим простой пример параметризованного теста:

import pytest

@pytest.mark.parametrize("input_data, expected", [(1, 2), (2, 4), (3, 6)])
def test_multiply_by_two(input_data, expected):
    assert input_data * 2 == expected
    
В этом примере:

- Мы параметризируем тест с двумя параметрами: `input` и `expected`
- Тест запустится три раза с разными наборами данных: (1, 2), (2, 4), (3, 6)
- Каждый запуск теста будет отображаться как отдельный тест в отчете

Нюансы и частые ошибки
    1. Синтаксис строки параметров

Правильно: имена параметров записываются через запятую без пробелов:
@pytest.mark.parametrize("param1,param2", [(1, 2), (3, 4)])

Неправильно: имена параметров с пробелами:
@pytest.mark.parametrize("param1, param2", [(1, 2), (3, 4)])  # Вызовет ошибку!

    2. Несоответствие количества параметров
Количество параметров в строке должно соответствовать количеству значений в кортежах:

# Правильно:
@pytest.mark.parametrize("a,b,c", [(1, 2, 3), (4, 5, 6)])

# Неправильно:
@pytest.mark.parametrize("a,b", [(1, 2, 3), (4, 5)])  # Ошибка!

    3. Использование одного параметра
Если у вас только один параметр, все равно нужно использовать список значений, а не один элемент:

# Правильно:
@pytest.mark.parametrize("user_id", [1, 2, 3])

# Неправильно:
@pytest.mark.parametrize("user_id", 1)  # Ошибка!


### Параметризация тестовых классов

Параметризация не ограничивается только отдельными тестовыми функциями. 
В pytest можно параметризовать целые тестовые классы, что очень удобно, когда нужно выполнить серию тестов с одинаковыми входными данными. 
Рассмотрим это на схематических примерах

### Основы параметризации тестовых классов

Для параметризации целого класса используется декоратор `@pytest.mark.parametrize` на уровне класса:

import pytest

@pytest.mark.parametrize("parameter_name", ["value1", "value2"])
class TestParametrizedClass:
    def test_first(sels, parameter_name):
        print(f"Тест 1 прогон: {parameter_name}")
        assert True
    
    def test_second(self, parameter_name):
        print(f"тест 2 прогон: {parameter_name})
        assert True

В этом примере каждый метод внутри класса `TestParametrizedClass` будет запущен дважды - один раз с `parameter_name="value1"` и один раз с `parameter_name="value2"`.

Попробуйте это выполнить этот код и посмотреть результат!
можете еще и с дебаггером попробовать


## Как это работает технически

Когда применяется декоратор `@pytest.mark.parametrize` к классу:

1. pytest создает несколько экземпляров класса (по одному для каждого набора параметров)
2. Каждый метод теста в классе получает доступ к соответствующим параметрам
3. Параметры становятся доступными как аргументы тестовых методов
4. Каждый тестовый метод запускается отдельно для каждого набора параметров

import pytest

@pytest.mark.parametrize("param_a,param_b", [
    ("a1", "b1"),
    ("a2", "b2")
])
class TestMultipleParams:

    def test_params_compination(self, param_a, param_b):
        print(f"1 тест: {param_a} и {param_b}")

    def test_another_method(self, param_a, param_b):
        combined = f"{param_a}-{param_b}"
        print(f"2 тест: {combined}")
        assert len(combined) > 2

Вы можете комбинировать параметризацию на уровне класса и метода:

import pytest

@pytest.mark.parametrize("class_param", ["c1", "c2"])
class TestCombinedParametrization:

    @pytest.mark.parametrize("method_param", ["m1", "m2", "m3"])
    def test_combination(self, class_param, method_param):
    # Этот тест запустится 6 раз (2 параметра класса × 3 параметра метода)
        print(f"Тест 1 с параметризацией класса={class_param} и метода={method_param}")
        assert True

    def test_only_class_param(self, class_param):
    # Этот тест запустится 2 раза (только с параметрами класса)
        print(f"Тест 2 с параметризацией только класса={class_param}")
        assert True

В этом примере:

- `test_combination` будет запущен 6 раз (все комбинации параметров)
- `test_only_class_param` будет запущен 2 раза (только с параметрами класса)


Пример с пропуском тестов на основе параметров

import pytest

@pytest.mark.parametrize(f"feature_flag,platform", [
    ("feature_a", "windows"),
    ("feature_a", "mac"),
    ("feature_b", "windows"),
    pytest.param("feature_b", "mac", marks=pytest.mark.skip(reason="Not supported on Mac"))
])
class TestFeatures:

    def test_feature_availability(self, feature_flag, platform):
        print(f"Testing {feature_flag} on {platform}")
        assert True

### **Использование `ids` для читаемого вывода**

По умолчанию Pytest отображает параметры как `[value1-value2-value3]`.

Можно задать **читаемые имена** для тестов с `ids`:
"""

# import pytest
# from .resources.user_creds import SuperAdminCreds
#
# @pytest.mark.parametrize("email,password,expected_status", [
#     (f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}", (200, 201)),
#     ("test_login@email.com", "asdqwe123Q!", 500),   # Сервис не может отработать логин по незареганному юзеру
#     ("","password", 500),
# ], ids=["Admin login", "Invalid user", "Empty username"])
# def test_login(email, password, expected_status, api_manager):
#     login_data = {
#         "email": email,
#         "password": password
#     }
#     api_manager.auth_api.login_user(login_data=login_data, expected_status=expected_status)

"""
Аннотации в Python – это **специальные подсказки для программиста и инструментов**, которые показывают, 
какие **типы данных** ожидаются в аргументах функций и что функция должна вернуть. **Python не заставляет их соблюдать**, 
но они делают код **понятнее, безопаснее и удобнее**.

Давай разберёмся, зачем они нужны, как работают и в чём их польза.
### Что такое аннотации и зачем они нужны?**

Представь, что у тебя есть функция:
def add(a, b):
    return a + b

Какой тип данных ожидается у a и b? 
Это могут быть:
Целые числа (int) → add(2, 3) # 5
Строки (str) → add("Hello", " World") # "Hello World"
Списки (list) → add([1, 2], [3, 4]) # [1, 2, 3, 4]
Но если кто-то случайно передаст число и строку?
add(5, "hello")  # TypeError: unsupported operand type(s)

Ошибка появится **во время выполнения**. А если у нас сложный код, где непонятно, какие аргументы передавать?

**Аннотации помогают избежать таких ситуаций!** Они говорят программисту: *"Эй, эта функция должна получать числа и возвращать число."*

В Python мы можем указывать типы с помощью **аннотаций**. Это **не строгая проверка**, а лишь "подсказка" для нас и инструментов анализа кода.

### **Простые аннотации**

def add(a: int, b: int) -> int:
    return a + b

- `a: int` обозначает, что `a` должен быть целым числом (`int`)
- `b: int` обозначает, что `b` должен быть целым числом (`int`)
- `-> int` обозначает, что  функция должна вернуть целое число

Посмотрим как это выглядит в редакторе кода

При попытки обращения функции и наведении на нее курсора, появится подсказка:


### **Аннотации для коллекций**

Что если функция принимает список? Используем `List` из модуля `typing`:

from typing import List

def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)

Или, например: 

from typing import Dict, Tuple, Set

def user_info() -> Dict[str, int]:
    return {"age": 25, "height": 180}

def get_coordinates() -> Tuple[float, float]:
    return (55.7558, 37.6173)  # Москва: широта, долгота

def unique_numbers(numbers: Set[int]) -> Set[int]:
    return set(numbers)

Хинт `:list` `:set` `:tuple` `:dict` без необходимости импортировать из `typing` появился в **Python 3.9**.

До этого, в **Python 3.5–3.8**, использовали из `typing`:

Начиная с Python 3.9, можно просто писать:
def func(numbers: list[int]) -> list[int]:
    return numbers


### **Аннотации для классов**

Аннотации работают и в классах:

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"
        
Теперь сразу видно, что name – строка, а age – число. Код стал самодокументируемым!

### **Когда значение может быть `None`**

Если функция может вернуть **значение или `None`**, используем `Optional`:

from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    Return None
Optional[str] значит, что функция вернёт либо str, либо None.


### **Использование `Union`**

Если аргумент может быть **разных типов**, используем `Union`:

from typing import Union

def process_input(value: Union[int, str]) -> str:
    return f"Ты передал: {value}"

Union[int, str] значит, что можно передавать и числа, и строки.
"""
