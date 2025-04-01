import os

BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIE_ENDPOINT = "/movies"
USER_ENDPOINT = "/user"
RED = "\033[31m"   # Красный цвет
GREEN = "\033[32m" # Зеленый цвет
RESET = "\033[0m"  # Сброс цвета (для возврата к обычному цвету текста)