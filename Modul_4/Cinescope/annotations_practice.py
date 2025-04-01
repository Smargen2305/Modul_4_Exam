
#1. Простые аннотации
def multiple(a :int, b :int) -> int:
    return a * b

x = multiple(3, 1)
print(x)

#2. Работа с коллекциями
from typing import List

def sum_numbers(numbers :List[int]) -> int:
    return sum(numbers)

x = sum_numbers([1, 2, 3, 4])
print(x)

#3. Используем Optional
from typing import Optional

def find_user(user_id :int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None

x = find_user(2)
print(x)

#4. Используем Union
from typing import Union

def process_input(value :Union[int, str]) -> str:
    return f"Ты передал: {value}"

x = process_input(1)
print(x)

#5. Работа с классами

class User:
    def __init__(self, name :str, age :int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}"

x = User("Aртем", 25)
print(x.greet())