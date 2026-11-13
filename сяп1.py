#задание 1
    # lst = [1, 2, 3, 4, 5]
    # k = 7
    # print("До сдвига:", lst)
    # shift = k % len(lst)
    # for _ in range(shift):
    #     lst.append(lst.pop(0))
    # print("После сдвига:", lst)

#задание 2

# s1={"Иванов", "Петров", "Сидоров"}
# s2={"Петров", "Сидоров", "Кузнецов"}
# print("те кто ходят на оба занятия",s1&s2,end="\n")
# print("те кто ходят на первое заняите ",s1-s2,end="\n")
# print("те кто ходят на второе  заняите ",s2-s1,end="\n")

#задание 3

brackets_map = {")": "(", "}": "{", "]": "["}
stack = []

# a = input("введите строку: ")
# is_valid = True
# for char in a:
#     if char in brackets_map.values():
#         stack.append(char)
#
#     elif char in brackets_map:
#         if not stack or stack.pop() != brackets_map[char]:
#             is_valid = False
#             break
#
# if is_valid and not stack:
#     print("все нормально ")
# else:
#     print("ошибка ")

# #задание 4
#
# words = ["кот", "ток", "дом", "мод", "сад"]
# groups = {}
# for word in words:
#     key = tuple(sorted(word))
#     if key not in groups:
#         groups[key] = []
#     groups[key].append(word)
# print("Все группы (словарь):")
# print(groups)
# filtered = {}
# for key, value in groups.items():
#     if len(value) >= 2:
#         filtered[key] = value
# sgroups = sorted(filtered.items(), key=lambda item: len(item[1]), reverse=True)
#
# print("\nТолько группы из 2+ слов, по убыванию размера:")
# for key, value in sgroups:
#     print(f"{key}: {value}")


#задание 5
cars = {
    "Skoda Octavia": ("Седан, 1.5 л, механика", 24900, 3),
    "Kia Sportage": ("Кроссовер, 2.0 л, автомат", 33500, 2),
    "Hyundai Solaris": ("Седан, 1.6 л, автомат", 18700, 5),
    "Toyota Camry": ("Седан, 2.5 л, автомат", 41200, 1),
}

while True:
    print("\nАВТОСАЛОН ")
    print("1 – Просмотр описания")
    print("2 – Просмотр цены")
    print("3 – Просмотр количества")
    print("4 – Вся информация об автомобиле")
    print("5 – Покупка")
    print("0 – Выход")

    choice = input("Выберите пункт меню: ").strip()
    if choice == "1":
        print("\n-- Описания автомобилей --")
        for name, info in cars.items():
            print(f"{name} – {info[0]}")

    elif choice == "2":
        print("\n-- Цены на автомобили --")
        for name, info in cars.items():
            print(f"{name} – {info[1]} руб.")

    elif choice == "3":
        print("\n-- Количество автомобилей в наличии --")
        for name, info in cars.items():
            print(f"{name} – {info[2]} шт.")

    elif choice == "4":
        print("\nПолная информация об автомобилях ")
        for name, info in cars.items():
            description, price, quantity = info
            print(f"{name}: {description}, цена {price} руб., в наличии {quantity} шт.")

    elif choice == "5":
        print("\nПокупка автомобиля")
        name = input("Введите название автомобиля: ").strip()

        if name not in cars:
            print("Ошибка: такой модели нет в автосалоне.")
            continue

        description, price, quantity = cars[name]

        amount_str = input("Введите количество единиц: ")
        if not str.isdigit():
            print("Ошибка: количество должно быть целым положительным числом.")
            continue
        amount = int(str)

        if amount <= 0:
            print("Ошибка: количество должно быть положительным числом.")
            continue

        if amount > quantity:
            print(f"Ошибка: недостаточно автомобилей в наличии (доступно {quantity} шт.)")
            continue

        total_cost = price * amount

        paid_str = input(f"Введите внесённую сумму (нужно {total_cost} руб.): ")
        if not paid_str.isdigit():
            print("Ошибка: сумма должна быть целым положительным числом.")
            continue
        paid = int(paid_str)

        if paid < total_cost:
            print(f"Ошибка: недостаточно средств. Не хватает {total_cost - paid} руб.")
            continue

        change = paid - total_cost
        cars[name] = (description, price, quantity - amount)

        print("\n===== ЧЕК =====")
        print(f"Модель: {name}")
        print(f"Количество: {amount} шт.")
        print(f"Цена за единицу: {price} руб.")
        print(f"Итоговая стоимость: {total_cost} руб.")
        print(f"Внесённая сумма: {paid} руб.")
        print(f"Сдача: {change} руб.")
  

    elif choice == "0":
        print("Выход из программы.")
        break

    else:
        print("Ошибка: некорректный пункт меню, попробуйте ещё раз.")