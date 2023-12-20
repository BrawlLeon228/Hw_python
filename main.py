import json
import types

import telebot
from config import BOT_TOKEN
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)
#@IntermediateCertificationBot - Имя бота


def search(message):
    bot.send_message(message.chat.id, 'Введите имя, фамилию через пробел:')
    bot.register_next_step_handler(message, searching)


def delete(message):
    bot.send_message(message.chat.id, 'Введите имя, фамилию через пробел:')
    bot.register_next_step_handler(message, deleting)


def change(message):
    bot.send_message(message.chat.id, 'Введите номер контакта, имя, фамилию и номера через пробел:')
    bot.register_next_step_handler(message, changing)


def load(message):
    bot.send_message(message.chat.id, 'Введите имя, фамилию и номера через пробел:')
    bot.register_next_step_handler(message, loading)


def look(message):
    for i in phone_book:
        bot.send_message(message.chat.id, f'{i}: {phone_book[i]}')


def save(message):
    bot.send_message(message.chat.id, 'Введите имя, фамилию и номера через пробел:')
    bot.register_next_step_handler(message, saving)


count = 1
phone_book = {"1": {
    'Имя': "Имя1",
    "Фамилия": "Фамилия1",
    "Phones": [222, 333]
    }
    }


@bot.message_handler(commands=['start'])
def stat_handler(message):
    bot.send_message(message.chat.id,
                     'Я твой телефонный справочник.\n\n'
                     'Чтобы узнать, что я могу введи команду /commands'
                     )


@bot.message_handler(commands=['commands'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Посмотреть номера'))
    markup.add(types.KeyboardButton('Добавить номер'))
    markup.add(types.KeyboardButton('Загрузить номер'))
    markup.add(types.KeyboardButton('Поиск'))
    markup.add(types.KeyboardButton('Удалить номер'))
    markup.add(types.KeyboardButton('Именить номер'))

    bot.send_message(message.chat.id, 'Выберете команду',
                     reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler()
def on_click(message):
    if message.text == 'Посмотреть номера':
        look(message)
    elif message.text == 'Добавить номер':
        save(message)
    elif message.text == 'Загрузить номер':
        load(message)
    elif message.text == 'Поиск':
        search(message)
    elif message.text == 'Удалить номер':
        delete(message)
    elif message.text == 'Именить номер':
        change(message)


@bot.message_handler()
def saving(message):
    global count
    data = message.text.split(' ')

    count += 1
    name = data[0]
    surname = data[1]
    print(name, surname)
    phones = []
    for i in range(2, len(data)):
        phones.append(int(data[i]))

    phone_book[count] = {"Имя": name, "Фамилия": surname, "Phones": phones}


@bot.message_handler()
def loading(message):
    global count
    data = message.text.split(' ')
    name = data[0]
    surname = data[1]
    phones = []
    count += 1
    for i in range(2, len(data)):
        phones.append(int(data[i]))

    contact = {count: {"Имя": name, "Фамилия": surname, "Phones": phones}}
    phone_book[count] = {"Имя": name, "Фамилия": surname, "Phones": phones}
    with open('Hw_python/contents.json', 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(contact, ensure_ascii=False))
    bot.send_message(message.chat.id, "Контакт успешно сохранен")


@bot.message_handler()
def searching(message):
    data = message.text.split(' ')
    name = data[0]
    surname = data[1]
    k = 0
    for i in phone_book:
        if phone_book[i]["Имя"] == name and phone_book[i]["Фамилия"] == surname:
            k = 1
            bot.send_message(message.chat.id, f'{i} {phone_book[i]}')
    if k == 0:
        bot.send_message(message.chat.id, 'Нет контакта с таким именем и фамилией')


@bot.message_handler()
def changing(message):
    data = message.text.split(' ')
    id_ = data[0]
    name = data[1]
    surname = data[2]
    phones = []
    k = 0
    for i in range(3, len(data)):
        phones.append(int(data[i]))
    for i in phone_book:
        if i == id_:
            k = 1
            phone_book[i] = {"Имя": name, "Фамилия": surname, "Phones": phones}
    if k == 0:
        bot.send_message(message.chat.id, "Нет контакта с таким именем и фамилией")


@bot.message_handler()
def deleting(message):
    data = message.text.split(' ')
    name = data[0]
    k = 0
    try:
        for i in phone_book:
            if phone_book[i]["Имя"] == name:
                k = 1
                surname1 = data[1]
                if phone_book[i]["Фамилия"] == surname1:
                    phone_book.pop(i)
                    bot.send_message(message.chat.id, "Контакт успешно удален")
    except RuntimeError:
        pass
    if k == 0:
        bot.send_message(message.chat.id, "Нет контакта с таким именем")


bot.polling(none_stop=True)
