import telebot
import ast
import time
from telebot import types


# модуль для работы с базой данныхq
import sqlite3
from datetime import datetime, timezone, timedelta


bot = telebot.TeleBot("6661527759:AAGXDtVjWVPnhsBDVFFyP9DN_uzc5cCJno8")




# Создайте таблицу пользователей, если она еще не существует
conn = sqlite3.connect("users.db")


olympiks = ["one", "two", "thre", "four", "five"]
save_olympiks = []
index = 0
delete_ol = ""
username = ""




@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    button_log = types.InlineKeyboardButton(
        text="Вход в систему", callback_data="login"
    )
    button_reg = types.InlineKeyboardButton(
        text="Регистрация в системе", callback_data="reg"
    )
    markup.add(button_log, button_reg)
    bot.send_message(
        message.chat.id,
        "Привет👋 , я Competitioner бот! Я помогу тебе с выбором олимпиады и напомню о ее начале в удобное время.\nНажми на одну из появившихся кнопок:",
        reply_markup=markup,
    )




@bot.callback_query_handler(func=lambda call: call.data == "reg")
def register(call):
    # Запросите у пользователя логин
    bot.send_message(call.message.chat.id, "Введите свой логин:")


    # Установите состояние пользователя на "ввод логина"
    bot.set_state(call.message.chat.id, "username")




@bot.message_handler(func=lambda message: bot.get_state(message.chat.id) == "username")
def get_username(message):
    # Получите логин пользователя и запросите пароль
    global username
    username = message.text
    bot.send_message(message.chat.id, f"Введите пароль для логина {username}:")


    # Установите состояние пользователя на "ввод пароля"
    bot.set_state(message.chat.id, "password")




@bot.message_handler(func=lambda message: bot.get_state(message.chat.id) == "password")
def get_password(message):
    # Получите пароль пользователя и зарегистрируйте его
    global username
    password = message.text
    register_user(message.chat.id, username, password)


    # Удалите состояние пользователя
    bot.delete_state(message.chat.id)


    # Сообщите пользователю об успешной регистрации
    bot.send_message(message.chat.id, "Регистрация прошла успешно!")




def register_user(user_login, username, password):
    # Вставьте нового пользователя в базу данных
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
        (user_login, username, password),
    )
    conn.commit()




@bot.callback_query_handler(func=lambda call: call.data == "login")
def login(call):
    # Запросите у пользователя логин
    bot.send_message(call.message.chat.id, "Введите свой логин:")


    # Установите состояние пользователя на "ввод логина"
    bot.set_state(call.message.chat.id, "username_log")




# Обработайте ввод логина
@bot.message_handler(
    func=lambda message: bot.get_state(message.chat.id) == "username_log"
)
def get_username(message):
    # Получите логин пользователя и запросите пароль
    global username
    username = message.text
    bot.send_message(message.chat.id, f"Введите пароль для логина {username}:")


    # Установите состояние пользователя на "ввод пароля"
    bot.set_state(message.chat.id, "password_log")




# Обработайте ввод пароля
@bot.message_handler(
    func=lambda message: bot.get_state(message.chat.id) == "password_log"
)
def get_password(message):
    # Получите пароль пользователя и проверьте его
    global username


    password = message.text
    user_id = check_credentials(username, password)


    # Если пользователь авторизован
    if user_id:
        # Сообщите пользователю об успешной авторизации
        bot.send_message(message.chat.id, "Вы успешно авторизовались!")
    # Если пользователь не авторизован
    else:
        # Сообщите пользователю о том, что данные введены неверно
        bot.send_message(
            message.chat.id, "Неверные данные для входа. Попробуйте еще раз."
        )


    # Удалите состояние пользователя
    bot.delete_state(message.chat.id)




# Функция для проверки учетных данных пользователя
def check_credentials(username, password):
    # Выполните запрос к базе данных для поиска пользователя с указанными учетными данными
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?", (username, password)
    )
    result = cursor.fetchone()
    conn.commit()


    # Если пользователь найден, верните его идентификатор
    if result:
        return result[0]
    # Если пользователь не найден, верните None
    else:
        return None




@bot.message_handler(commands=["about"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_add = types.KeyboardButton("Добавить олимпиаду")
    button_mine = types.KeyboardButton("Список добавленных олимпиад")
    markup.add(button_add, button_mine)
    bot.send_message(
        message.chat.id,
        "Привет👋 , я Competitioner бот! Я помогу тебе с выбором олимпиады и напомню о ее начале в удобное время.",
        reply_markup=markup,
    )




@bot.message_handler(commands=["add"])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    for ol in olympiks:
        markup.add(types.InlineKeyboardButton(text=f"{ol}", callback_data=ol))
    bot.send_message(message.chat.id, "Список всех олимпиад:", reply_markup=markup)




@bot.message_handler(content_types="text")
def message_reply(message):
    if message.text == "Добавить олимпиаду":
        markup = types.InlineKeyboardMarkup()
        for ol in olympiks:
            markup.add(types.InlineKeyboardButton(text=f"{ol}", callback_data=ol))
        bot.send_message(message.chat.id, "Список всех олимпиад:", reply_markup=markup)


    elif message.text == "Список добавленных олимпиад":
        if save_olympiks:
            markup = types.InlineKeyboardMarkup()
            for ol in save_olympiks:
                markup.add(
                    types.InlineKeyboardButton(text=f"{ol}", callback_data="save" + ol)
                )
            bot.send_message(
                message.chat.id, "Список моих олимпиад:", reply_markup=markup
            )
        else:
            bot.send_message(message.chat.id, "Список пуст 😞.")


    elif message.text == "Да":
        save_olympiks.append(olympiks[index])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add = types.KeyboardButton("Добавить олимпиаду")
        button_mine = types.KeyboardButton("Список добавленных олимпиад")
        markup.add(button_add, button_mine)
        bot.send_message(
            message.chat.id, "Олимпиада добавлена в список 🥳.", reply_markup=markup
        )


    elif message.text == "Нет":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add = types.KeyboardButton("Добавить олимпиаду")
        button_mine = types.KeyboardButton("Список добавленных олимпиад")
        markup.add(button_add, button_mine)
        bot.send_message(message.chat.id, "ok", reply_markup=markup)


    elif message.text == "Удалить":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add = types.KeyboardButton("Добавить олимпиаду")
        button_mine = types.KeyboardButton("Список добавленных олимпиад")
        markup.add(button_add, button_mine)
        save_olympiks.remove(delete_ol)
        bot.send_message(
            message.chat.id, "Олимпиада удалена из списка.", reply_markup=markup
        )


    elif message.text == "Оставить все как есть":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add = types.KeyboardButton("Добавить олимпиаду")
        button_mine = types.KeyboardButton("Список добавленных олимпиад")
        markup.add(button_add, button_mine)
        bot.send_message(message.chat.id, "Ок", reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Извлекаем элемент списка из callback_data
    element = call.data
    if "save" in element:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_delete = types.KeyboardButton("Удалить")
        button_no = types.KeyboardButton("Оставить все как есть")
        markup.add(button_delete, button_no)
        element = element[4:]
        global delete_ol
        delete_ol = element
        bot.send_message(
            call.message.chat.id,
            f"Описание олимпиады:{element}, inex = {olympiks.index(element)}",
            reply_markup=markup,
        )
    else:
        global index
        index = olympiks.index(element)
        bot.send_message(
            call.message.chat.id,
            f"Описание олимпиады:{element}, inex = {olympiks.index(element)}\nДобавить олимпиаду в список выбранных?",
        )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_yes = types.KeyboardButton("Да")
        button_no = types.KeyboardButton("Нет")
        markup.add(button_yes, button_no)
        bot.send_message(
            call.message.chat.id,
            "Добавить олимпиаду в список выбранных?",
            reply_markup=markup,
        )




while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)