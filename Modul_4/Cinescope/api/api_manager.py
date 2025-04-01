from .auth_api import AuthAPI
from .user_api import UserAPI
from .films_api import MoviesAPI


# from Modul_4.Cinescope.api.user_api import UserAPI

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.films_api = MoviesAPI(session)
        self.user_api = UserAPI(session)

    # Добавили в класс ApiManager новый метод, который закрывает переданную в него сессию, чтобы фикстура def user_session() работала:
    def close_session(self):
        self.session.close()
