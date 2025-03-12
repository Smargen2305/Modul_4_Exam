from faker import Faker
import pytest
import requests
from .constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, MOVIE_ENDPOINT
from .custom_requester.custom_requester import CustomRequester
from .utils.data_generator import DataGenerator
from .api.auth_api import AuthAPI
from .api.api_manager import ApiManager

faker = Faker()

@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,  # Убедимся, что password и passwordRepeat совпадают
        "roles": ["USER"]
    }
@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    # Регистрируем пользователя
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()

    # Обновляем данные пользователя (включаем ID из ответа регистрации)
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]

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
        "email": "test-admin@mail.com",
        "password": "KcLMmxkJMjBD1"
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
