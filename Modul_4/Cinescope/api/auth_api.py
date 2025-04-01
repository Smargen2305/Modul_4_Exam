from ..custom_requester.custom_requester import CustomRequester
from ..constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT
from ..resources.user_creds import SuperAdminCreds

class AuthAPI(CustomRequester):
    """
      Класс для работы с аутентификацией.
      """

    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def get_user(self, locator, expected_status=200):
        """
        Получение данных пользователя по email или ID.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/user/{locator}",
            expected_status=expected_status
        )

    def authentication_user(self, creds=None, expected_status=200):
        """
        Авторизует Super_Admin и обновляет заголовки сессии токеном.
        :param expected_status:
        :return: Токен.
        """
        if creds is None:
            creds = {"email": SuperAdminCreds.USERNAME, "password": SuperAdminCreds.PASSWORD}
        elif isinstance(creds, tuple):
            creds = {"email": creds[0], "password": creds[1]}
        response = self.login_user(creds, expected_status)
        token = response.json()["accessToken"]
        print(token)
        self._update_session_headers(Authorization=f"Bearer {token}")
        return token
