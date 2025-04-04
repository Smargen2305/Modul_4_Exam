
#
#     ### Описание темы: Вставка значений в строку
#
#     В Python можно вставлять значения в строки, используя различные методы форматирования. Это полезно для динамического формирования текста, например, для сообщений с переменными данными.
#
#     **Основные методы:**
#
#     - `f-строки` — позволяют вставлять переменные и выражения внутрь строки, используя синтаксис `f"..."`.
#     - Метод `.format()` — вставляет значения в строку, используя плейсхолдеры `{}`.
#     - Оператор `%` — более старый метод форматирования строк, который позволяет вставлять значения, используя символ `%`.
#
#     **Пример:**
#
#     ```python
#     name = "Анна"
#     age = 30
#
#     # f-строка
#     print(f"Привет, меня зовут {name}, и мне {age} лет.")  # Выведет: "Привет, меня зовут Анна, и мне 30 лет."
#
#     # Метод format
#     print("Привет, меня зовут {}, и мне {} лет.".format(name, age))  # Выведет: "Привет, меня зовут Анна, и мне 30 лет."
#
#     ```
#
#     ### Задания:
#
#     - **Задание #1**
#         1. Создайте переменные `name` со значением `"Дмитрий"` и `age` со значением `28`.
#         2. Вставьте значения переменных `name` и `age` в строку с помощью `f-строки`, и сохраните результат в переменную `greeting_f`. Проверьте результат.

name = "Дмитрий"
age = 28
greeting_f =  f"{name},{age}"
print(greeting_f)


#     - **Задание #2**
#         1. Создайте переменные `city` со значением `"Москва"` и `temperature` со значением `15.5`.
#         2. Вставьте значения переменных `city` и `temperature` в строку с помощью метода `.format()`, и сохраните результат в переменную `weather_format`. Проверьте результат.

city = "Москва"
temperature = 15.5

weather_format = "В городе {} сейчас температура {}°C.".format(city, temperature)
weather_format2= f'В городе {city} сейчас температура {temperature}°C.'
print(weather_format2)

#     - **Задание #3**
#         1. Создайте переменные `product` со значением `"ноутбук"` и `price` со значением `54999`.
#         2. Вставьте значения переменных `product` и `price` в строку с помощью оператора `%`, и сохраните результат в переменную `product_info_percent`. Проверьте результат.

product = "ноутбук"
price =  54999

product_info_percent = "Товар: %s, цена: %d рублей." % (product, price)

print(product_info_percent)
