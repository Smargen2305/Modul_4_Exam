import random
import string
from faker import Faker

faker = Faker()

class DataGenerator:
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"TesT{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        first_names = ["John", "Jane", "Alex", "Emily", "Chris"]
        last_names = ["Smith", "Doe", "Johnson", "Brown", "Davis"]
        random_first_name = random.choice(first_names)
        random_last_name = random.choice(last_names)
        return f"{random_first_name} {random_last_name}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*_-+()[]{}><\\/|\"'.,:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_movie_name():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        return f"фильм-{random_string}"

    @staticmethod
    def generate_random_movie_price():
        random_price = random.randint(0, 1000)
        return random_price

    @staticmethod
    def generate_random_movie_description():
        random_description = faker.sentence(nb_words=6)
        return random_description

    @staticmethod
    def generate_random_location():
        locations = ["MSK", "SPB"]
        random_locations = random.choice(locations)
        return random_locations
