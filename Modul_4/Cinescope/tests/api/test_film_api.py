from http.client import responses

from ...conftest import movie_data
from ....Cinescope.api.api_manager import ApiManager

class TestPositiveScenariosMovies:
    """
    Класс для проверки позитивных сценариев Movies
    """
    def test_get_movies(self,api_manager):
        """
        Тест для получения списка фильмов
        :param api_manager:
        :return:
        """
        response_data = api_manager.films_api.get_movies().json()

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

    def test_create_movie_by_super_admin(self, api_manager, movie_data):
        """
        Тест создание фильма под ролью SUPER_ADMIN
        :param api_manager:
        :return:
        """
        api_manager.auth_api.authentication_user()
        response_data = api_manager.films_api.create_movie(movie_data).json()

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

    def test_delete_movie_by_super_admin(self, api_manager, movie_data):

        # Получаем токен авторизации под ролью Super Admin
        api_manager.auth_api.authentication_user()

        # Создаем фильм для получения ID созданного фильма
        create_data = api_manager.films_api.create_movie(movie_data).json()
        movie_id = create_data["id"]
        print(f"ID фильма = {movie_id}")

        # Вызываем метод DELETE с переданным movie_id
        response = api_manager.films_api.delete_movie(movie_id)
        assert response.status_code == 200, "Фильм не удалился"

        # Вызываем метод GET для подтверждения того, что фильм удалился
        response_data = api_manager.films_api.get_movie(movie_id, expected_status=404)
        assert response_data.status_code == 404, "Фильм доступен по ID "



