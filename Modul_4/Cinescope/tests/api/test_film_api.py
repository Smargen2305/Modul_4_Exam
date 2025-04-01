import pytest
from http.client import responses

from ...conftest import movie_data, super_admin, common_user
from ....Cinescope.api.api_manager import ApiManager

class TestPositiveScenariosMovies:
    """
    Класс для проверки позитивных сценариев Movies
    """
    def test_get_movies(self,common_user):
        """
        Тест для получения списка фильмов
        :param api_manager:
        :return:
        """
        response_data = common_user.api.films_api.get_movies().json()

        assert "movies" in response_data, "Ключ movies отсутствует"
        assert "count" in response_data, "Ключ count отсутствует"
        assert "page" in response_data, "Ключ page отсутствует"
        assert "pageSize" in response_data, "Ключ pageSize отсутствует"
        assert "pageCount" in response_data, "Ключ pageCount отсутствует"

        for movie in response_data["movies"]:
            assert "id" in movie, "ID фильма не существует"
            assert "name" in movie, "Имя фильма не существует"
            assert "description" in movie, "Описание фильма не существует"
            assert "location" in movie, "Локация создания фильма не существует"
            assert "published" in movie, "Состояние публикации фильма отсутствует"
            assert "genre" in movie, "Жанр фильма отсутствует"
            assert "name" in movie["genre"], "Жанр фильма отсутствует"

    def test_create_movie_by_super_admin(self, super_admin, movie_data):
        """
        Тест создание фильма под ролью SUPER_ADMIN
        :param api_manager:
        :return:
        """
        response_data = super_admin.api.films_api.create_movie(movie_data).json()

        # Проверки
        assert "id" in response_data, "ID фильма не найдено"
        assert "createdAt" in response_data, "Дата создания фильма отсутствует"
        assert "rating" in response_data, "Рейтинг фильма отсутствует"
        assert "name" in response_data["genre"], "Жанр фильма отсутствует"

        assert response_data["name"] == movie_data["name"], "ИМЯ фильма не совпадает"
        assert response_data["price"] == movie_data["price"], "ЦЕНА фильма не совпадает"
        assert response_data["description"] == movie_data["description"], "ОПИСАНИЕ фильма не совпадает"
        assert response_data["location"] == movie_data["location"], "ЛОКАЦИЯ фильма не совпадает"
        assert response_data["published"] == movie_data["published"], "ЛОКАЦИЯ фильма не совпадает"
        assert response_data["genreId"] == movie_data["genreId"], "ЛОКАЦИЯ фильма не совпадает"

    def test_delete_movie_by_super_admin(self, super_admin, movie_data, common_user, role, status_code):

        # Получаем токен авторизации под ролью Super Admin
        # api_manager.auth_api.authentication_user()

        # Создаем фильм для получения ID созданного фильма
        create_data = super_admin.api.films_api.create_movie(movie_data).json()
        movie_id = create_data["id"]

        # Вызываем метод DELETE с переданным movie_id
        response = super_admin.api.films_api.delete_movie(movie_id)
        assert response.status_code == 200, "Фильм не удалился"

        # Вызываем метод GET для подтверждения того, что фильм удалился
        response_data = common_user.api.films_api.get_movie(movie_id, expected_status=404)
        assert response_data.status_code == 404, "Фильм доступен по ID "

    def test_create_movie_by_common_user(self, common_user, movie_data):
        # тест, в котором запрос будет происходить от юзера с ролью USER
        # Мы будем ожидать ответ от сервера 403 forbidden на попытку создания
        assert common_user.roles == ["USER"], f"Ожидалась роль USER, но получено {common_user.roles}"
        response_data = common_user.api.films_api.create_movie(movie_data, expected_status=403)

    def test_create_movie_by_admin(self, admin_user, movie_data):
        """
        Тест создание фильма под ролью SUPER_ADMIN
        :param api_manager:
        :return:
        """
        response_data = admin_user.api.films_api.create_movie(movie_data).json()

        # Проверки
        assert "id" in response_data, "ID фильма не найдено"
        assert "createdAt" in response_data, "Дата создания фильма отсутствует"
        assert "rating" in response_data, "Рейтинг фильма отсутствует"
        assert "name" in response_data["genre"], "Жанр фильма отсутствует"

        assert response_data["name"] == movie_data["name"], "ИМЯ фильма не совпадает"
        assert response_data["price"] == movie_data["price"], "ЦЕНА фильма не совпадает"
        assert response_data["description"] == movie_data["description"], "ОПИСАНИЕ фильма не совпадает"
        assert response_data["location"] == movie_data["location"], "ЛОКАЦИЯ фильма не совпадает"
        assert response_data["published"] == movie_data["published"], "ЛОКАЦИЯ фильма не совпадает"
        assert response_data["genreId"] == movie_data["genreId"], "ЛОКАЦИЯ фильма не совпадает"

    @pytest.mark.parametrize("minPrice,maxPrice,locations,genreId", [
        (1, 500, "MSK", 1),
        (2, 999, "SPB", 2),
        (1, 1000, "MSK", 1)
    ], ids=["price_1-500_msk_drama",
            "price_2-999_spb_comedy",
            "price_1-1000_msk_drama"])
    def test_get_movies_by_filters(self, minPrice, maxPrice, locations, genreId, super_admin):
        # Формируем параметры для запроса
        params ={
            "minPrice": minPrice,
            "maxPrice": maxPrice,
            "locations": locations,
            "genreId": genreId
        }
        # Отправляем запрос с параметрами
        response = super_admin.api.films_api.get_movies(params=params, expected_status=200)
        response_data = response.json()

        # Проверяем, что фильмы соответствуют фильтрам
        for movie in response_data["movies"]:
            assert minPrice <= movie["price"] <= maxPrice, f"Цена фильма {movie['price']} не в диапазоне [{minPrice}, {maxPrice}]"
            assert movie["location"] == locations, f"Локация фильма {movie['location']} не соответствует ожидаемой {locations}"
            assert movie["genreId"] == genreId, f"ID жанра фильма {movie['genreId']} не соответствует ожидаемому {genreId}"

    @pytest.mark.parametrize("user_fixture,status_code", [
        ("super_admin", 200),
        ("admin_user", 403),
        ("common_user", 403)
    ], ids=["delete_by_SUPER_ADMIN",
            "delete_by_ADMIN",
            "delete_by_USER"])
    def test_delete_movie_by_all_roles(self, super_admin, user_fixture, movie_data, status_code, request):
        """
            Тест проверяет удаление фильма с учетом ролевой модели.
            - SUPER_ADMIN должен успешно удалить фильм (статус 200).
            - ADMIN и USER не должны иметь доступ к удалению (статус 403).
            """
        # Получаем пользователя по имени фикстуры, переданному в user_fixture
        user = request.getfixturevalue(user_fixture)

        # Создаем фильм с помощью super_admin, так как он имеет права на создание
        create_data = super_admin.api.films_api.create_movie(movie_data).json()
        movie_id = create_data["id"]  # Получаем ID созданного фильма

        # Вызываем метод DELETE с переданным movie_id
        response = user.api.films_api.delete_movie(movie_id, expected_status=status_code)
        assert response.status_code == status_code, f"Ожидался статус-код {status_code}, но получен {response.status_code}"