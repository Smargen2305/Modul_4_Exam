from ..constants import BASE_URL, MOVIE_ENDPOINT
from ..custom_requester.custom_requester import CustomRequester
from ...test_super_duper.tests.conftest import headers


class MoviesAPI(CustomRequester):
    """
    Класс для тестирования CRUD операций с movie(s)
    """
    def __init__(self, session):
        """
        Конструктор для инициализации базового URL и реквестера.
        """
        super().__init__(session=session, base_url = "https://api.dev-cinescope.coconutqa.ru/")


    def get_movies(self, params=None, expected_status=200, need_logging=True):
        """
        Получение списка фильмов с возможностью фильтрации.
        :param params: Словарь параметров для фильтрации.
        :return: Объект ответа.
        """
        # Реализуйте метод GET /movies
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}",
            params=params,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        """
        Получение данных о фильме по ID.
        :param movie_id: Идентификатор фильма.
        :return: Объект ответа.
        """
        # Реализуйте метод GET /movies/{id}
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        """
        Создание нового фильма.
        :param data: Словарь данных для создания фильма.
        :param token: Токен авторизации SUPER_ADMIN.
        :return: Объект ответа.
        """
        # Реализуйте метод POST /movies
        # headers = {"Authorization": f"Bearer {token}"}       # убрать благдаря authenticate
        return self.send_request(
            method="POST",
            endpoint=f"{MOVIE_ENDPOINT}",
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        Удаление фильма по ID.
        :param movie_id: Идентификатор фильма.
        :param token: Токен авторизации SUPER_ADMIN.
        :return: Объект ответа.
        """
        # Реализуйте метод DELETE /movies/{id}
        # headers = {"Authorization": f"Bearer {token}"}              # убрать благдаря authenticate
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )
