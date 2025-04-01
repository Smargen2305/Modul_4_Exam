from ..api.api_manager import ApiManager

class User:
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api      # Сюда будем передавать экземпляр API Manager для запросов

    @property
    def creds(self):
        """Возвращает кортеж (email, password)"""
        return self.email, self.password

"""
**Зачем это нужно?**

1. Описывает структуру пользователя. Мы можем в дальнейшем добавить новых параметров 
или добавить аттрибутов объектам и в тесте у нас будет объект текущего юзера (а точнее нескольких юзеров раздельно, чтобы не путать где какой)
2. Свойство creds позволит нам более удобно пользоваться аутентификацией юзера
3. Включает `api_manager` для выполнения API-запросов. То есть теперь мы будем отправлять запросы через юзера, у которого есть объект апи менеджера
"""

# Пояснение по классу

## 1. __init__
## def __init__(self, email: str, password: str, roles: list, api_manager):
"""
Этот метод вызывается при создании нового объекта `User`.

- `email: str` → строка с email пользователя.
- `password: str` → строка с паролем.
- `roles: list` → список ролей пользователя (например, `["USER"]`).
- `api_manager` → экземпляр `ApiManager`, который позволяет пользователю делать API-запросы.

Когда создаем пользователя, например:

user = User(email="test@example.com", password="123456", roles=["USER"], api_manager=api_manager)

Объект user будет содержать всю эту информацию.
"""

## 2. @property – Свойство creds
"""
@property
def creds(self):
    Возвращает кортеж (email, password)
    return self.email, self.password
"""

### Декоратор @property делает метод creds доступным как атрибут:
### print(user.creds)  ('test@example.com', '123456')

### Это удобно, так как не нужно вызывать метод, а можно просто обращаться к атрибуту:
### email, password = user.creds