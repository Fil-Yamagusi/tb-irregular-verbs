#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""2024-01-12 Fil - Future code Yandex.Practicum
Бот-квест "Экзамен по неправильным английским глаголам"
Описание в README.txt

Fil FC Quest: Irregular verbs
FC: Irregular Verbs Exam
@fil_fc_irregular_verbs_bot
https://t.me/fil_fc_berlin1884_bot
6414363219:AAFIznT89_9QZQNWAhFC4UqOqTaCxnZalhU
"""
__version__ = '0.1'
__author__ = 'Firip Yamagusi'

from time import time, strftime, sleep
from random import seed, randint, shuffle

from telebot import TeleBot
from telebot import types
from telebot.types import Message, User
import sqlite3

TOKEN = "6414363219:AAFIznT89_9QZQNWAhFC4UqOqTaCxnZalhU"
bot_name = "FC: Irregular Verbs Exam | @fil_fc_irregular_verbs_bot"
print(strftime("%F %T"))
print(bot_name)
print(TOKEN)

bot = TeleBot(TOKEN)

# Для простого хранения некоторых данных, чтобы не бегать в БД.
users = {}


# Создаём подключение к базе данных (файл berlin1884.db будет создан)
db = 'iv_score.db'
db_conn = sqlite3.connect(db, check_same_thread=False)
dbc = db_conn.cursor()


# Создаем таблицу Users
dbc.execute(
    'CREATE TABLE IF NOT EXISTS Users ('
    'uid INTEGER PRIMARY KEY, '
    'first_time INTEGER, '
    'last_time INTEGER'
    ')'
)


# Основное меню
menu_main = {
    'play': 'Начать игру',
    'help': 'Помощь',
}

keyboard_main = types.ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True
)
keyboard_main.add(*menu_main.values())

# Простое меню Да/Нет. Пригождается в разных ситуациях
menu_yes_no = {
    'yes': 'Да',
    'no': 'Нет',
}

keyboard_yes_no = types.ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True
)
keyboard_yes_no.add(*menu_yes_no.values())


@bot.message_handler(commands=['start'])
def handle_start(m: Message):
    """Приветствие, регистрация"""

    global users
    global db, db_conn, dbc

    # Ищем пользователя. Если не нашли, то создаём
    uid = m.from_user.id
    if uid not in users:
        users[uid] = {}

    try:
        dbc.execute('SELECT uid '
                    'FROM Users '
                    'WHERE uid=? LIMIT 1', (uid,))
        user_db = dbc.fetchone()

        # Если пользователь существует в базе, то берём оттуда.
        if user_db:
            pass
        # Иначе добавляем пользователя.
        else:
            dbc.execute("INSERT INTO Users "
                        "(uid) "
                        "VALUES (?)",
                        (m.from_user.id, ))
            print(f"Пользователь {uid} СОЗДАН. ")
            db_conn.commit()
    except Exception as e:
        print("Ошибка при добавлении нового пользователя")

    bot.send_message(
        m.from_user.id,
        f"<b>Сложная для психики игра, {m.from_user.first_name}!</b>\n\n"
        "В сюжете - зло, происходившее более 140 лет назад. Которое было "
        "более кровавым, чем обе мировые войны, ВМЕСТЕ ВЗЯТЫЕ. И беда в том, "
        "что оно продолжается до сих пор.\n\n"
        "Современные лидеры Европы ловко спрятались за Гитлером и его "
        "развитой теорией расового превосходства. Давай посмотрим, у кого "
        "Гитлер учился жестокости, и далеко ли он ушёл от учителей?\n\n"
        "В игре ты будешь представителем одной из 'цивилизованных' стран и "
        "повторишь раздел Чёрного континента. Никакой выдумки. Именно так "
        "решали судьбу Африке на Берлинской конференции 1884 года.\n\n"
        "Начать игру - /play\n"
        "Подробнее - в справке /help",

        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=keyboard_main
    )

    pic = 'pic/start-ai-' + str(randint(1, 5)) + '.jpg'
    with open(pic, 'rb') as pic_file:
        print(pic)
        bot.send_photo(
            m.from_user.id, pic_file,
            caption="Деловые люди делят 'африканский пирог'.\n"
                    "Если бы карикатуры могли их остановить...")


@bot.message_handler(
    content_types=["text"],
    func=lambda m: m.text == menu_main['play'])
@bot.message_handler(commands=['play'])
def handle_play(m: Message):
    """Принудительно запускаем новую игру"""

    msg = bot.send_message(
        m.from_user.id,
        f"Начинаем новую игру!\n\n",

        parse_mode="HTML",
        reply_markup=keyboard_main
    )


@bot.message_handler(
    content_types=["text"],
    func=lambda m: m.text == menu_main['help'])
@bot.message_handler(commands=['help'])
def handle_help(m: Message):
    """готовимся принять слово"""

    bot.send_message(
        m.from_user.id,
        f"ХОД ИГРЫ:\n\n"
        f"1) Выбор европейской страны-колонизатора.\n"
        f"2) Все страны-колонизаторы разыгрывают порядок выбора "
        f"первых колоний.\n"
        f"3) Выбор способа ограбления колонии.\n"
        f"4) Случайные события и изменение макроэкономических "
        f"показателей.\n"
        f"5) Промежуточная статистика.\n\n"
        f"Эти шаги повторяются ещё несколько раз. Когда территории "
        f"для колоний закончатся, выводится счёт и подводится итог\n\n"
        f"/start - Начальное приветствие\n"
        f"/play - Начало новой игры",

        parse_mode="HTML",
        reply_markup=keyboard_main
    )


bot.polling(none_stop=True)
