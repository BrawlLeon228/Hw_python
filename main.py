import json

import sqlite3 as sl


phone_book = {"Имя": {
    "Фамилия": "Фамилия1",
    "Phones": [89059834092, 555001]
    }
    }


def search():
    name = input("Введите имя: \n")
    k = 0
    for i in phone_book:
        if i == name:
            k = 1
            print(i, phone_book[i])
    if k == 0:
        print("Нет контакта с таким именем\n")


def delete():
    name = input("Введите имя: \n")
    k = 0
    try:
        for i in phone_book:
            if i == name:
                k = 1
                surname1 = input("Введите фамилию: \n")
                if phone_book[i]["Фамилия"] == surname1:
                    phone_book.pop(i)
    except RuntimeError:
        pass
    if k == 0:
        print("Нет контакта с таким именем\n")


def change():
    name = input("Введите имя: \n")
    k = 0
    for i in phone_book:
        if i == name:
            k = 1
            print("Введите новые данные:")
            name = input("Введите имя: \n")
            surname = input("Введите фамилию: \n")
            phones = input("Введите номера через пробел: \n").split(' ')
            phone_book[name] = {"Фамилия": surname, "Phones": phones}
    if k == 0:
        print("Нет контакта с таким именем")

def load():
    name = input("Введите имя: \n")
    surname = input("Введите фамилию: \n")
    phones = input("Введите номера через пробел: \n").split(' ')
    contact = {name: {"Фамилия": surname, "Phones": phones}}

    with open('contents.json', 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(contact, ensure_ascii=False))
    print("Контакт успешно сохранен")

def look():
    for i in phone_book.items():
        print(*i)
    print()


def save():
    name = input("Введите имя: \n")
    surname = input("Введите фамилию: \n")
    phones = input("Введите номера через пробел: \n").split(' ')
    phone_book[name] = {"Фамилия": surname, "Phones": phones}
    print()


func = 0
running = True
while running:
    try:
        func = int(input('Выберете действие: просмотр-1, сохранение-2, импорт-3, поиск-4, удаление-5, изменение данных-6\n'))
    except ValueError:
        pass

    if func == 1:
        look()
    elif func == 2:
        save()
    elif func == 3:
        load()
    elif func == 4:
        search()
    elif func == 5:
        delete()
    elif func == 6:
        change()
    else:
        pass
