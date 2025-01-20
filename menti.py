goblin_shop = {'Зелье лечения': 100,
                'Зелье маны': 80,
                'Свиток скорости': 150,
                'Артефакт магии': 300
                }
item = input('Товар: ')
quantity = int(input('Количество: '))

if item in goblin_shop:
    cost = quantity * goblin_shop[item]
    if cost > 500:
        cost *= 0.8
        print(f'Итоговая стоимость со скидкой: ', {cost})
    print(f'Итоговая стоимость: ', {cost})
else:
    print("Товара нет)") #dfdfdf