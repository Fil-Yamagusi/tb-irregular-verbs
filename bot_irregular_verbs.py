#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""2024-01-12 Fil - Future code Yandex.Practicum
Бот-квест "Экзамен по неправильным английским глаголам"
Описание в README.md

Fil FC Quest: Irregular verbs
FC: Irregular Verbs Exam
@fil_fc_irregular_verbs_bot
https://t.me/fil_fc_irregular_verbs_bot
6414363219:AAFIznT89_9QZQNWAhFC4UqOqTaCxnZalhU
"""
__version__ = '0.3'
__author__ = 'Firip Yamagusi'

# Для рандома внутри квеста
from time import time, strftime
from random import seed, randint, shuffle, choice
from os import path

from telebot import TeleBot
from telebot import types
from telebot.types import Message
import sqlite3

from db_functions import create_tables, insert_record
# Опросник для локации "Перед школой" (1 из 4)
from questions_loc_a import questions_a
# Сами неправильные глаголы "Перед экзаменом" (2, 3 из 4)
from questions_loc_b import verbs
# RPG-элементы квеста
from data import rpg_classes, rpg_items
# Массивы фрагментов для рандомизации фраз
from data import teacher_names, right_answer, three_forms, spooky
from data import how, why, friends, caricature

# Нужно для создания относительных путей к картинкам и к БД
script_dir = path.dirname(__file__)

TOKEN = "6414363219:AAFIznT89_9QZQNWAhFC4UqOqTaCxnZalhU"
bot_name = "FC: Irregular Verbs Exam | @fil_fc_irregular_verbs_bot"
# Для понимания в консоли
print(strftime("%F %T"))
print(bot_name)
print(TOKEN, "\n")

bot = TeleBot(TOKEN)

# Рандомно запускаем рандом для Великого бога RPG-рандома.
seed(time())

# Для простого хранения некоторых данных, чтобы не бегать в БД.
users = {}

# Создаём подключение к базе данных (файл iv_score.db будет создан).
db_conn = sqlite3.connect(
    path.join(script_dir, 'iv_score.db'),
    check_same_thread=False)

# Создаём таблицу Users для хранения параметров пользователей
create_tables(db_conn)


# Пустое меню, может пригодиться
hideKeyboard = types.ReplyKeyboardRemove()

# Основное меню
menu_main = {
    'play': 'Начать игру',
    'help': 'Справка',
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

# Однокнопочное меню Продолжаем. Чтобы успели прочитать сообщения.
menu_continue = {
    'continue': 'Продолжаем!',
}
keyboard_continue = types.ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True
)
keyboard_continue.add(*menu_continue.values())

# Однокнопочное меню Смирения. Для тупиковых положений.
menu_shtosh = {
    'shtosh': 'Ну штош...',
}
keyboard_shtosh = types.ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True
)
keyboard_shtosh.add(*menu_shtosh.values())


def check_user(uid: int, restart=False) -> bool:
    """Добавляем пользователя во временный словарь, чтобы БД не мучить"""
    global users

    if uid not in users or restart:
        zero_params = [
            # Основные rpg-параметры.
            'p_hearing', 'p_vision', 'p_dexterity', 'p_logic',
            # Номер последнего заданного вопроса в локации a (1),
            # номер последнего заданного глагола из verbs в локации b (2),
            # номер последнего заданного глагола из verbs в локации c (3).
            'q_loc_a', 'q_loc_b', 'q_loc_c',
            # Сколько уже ответил вопросов в локациях b, c. И сколько правильно.
            'q_num_b', 'q_num_b_ok', 'q_num_c', 'q_num_c_ok'
        ]
        users[uid] = {}
        # Название локации, в которой данный пользователь
        users[uid]['next_location'] = 'a'
        users[uid]['rpg_class'] = 'geek'
        for z in zero_params:
            users[uid][z] = 0
        users[uid]['item_is_used'] = 0
        users[uid]['result'] = 'DNF'
        return False


def normalize_rpg_params(uid: int) -> None:
    """RPG-параметры должны быть от 0 до 20"""
    global users

    users[uid]['p_hearing'] = min(max(0, users[uid]['p_hearing']), 20)
    users[uid]['p_vision'] = min(max(0, users[uid]['p_vision']), 20)
    users[uid]['p_dexterity'] = min(max(0, users[uid]['p_dexterity']), 20)
    users[uid]['p_logic'] = min(max(0, users[uid]['p_logic']), 20)


def show_random_picture(
        msg: Message, prefix: str, n_from: int, n_to: int, capt: str):
    """Показываем случайную картинку из нескольких для данного случая"""
    global script_dir

    # Было красивее, но python7 masterhost ругается
    pict = path.join(script_dir,
                        f"pic/{prefix}-" + str(randint(n_from, n_to)) + ".jpg")
    with open(pict, 'rb') as pic_file:
        bot.send_photo(
            msg.from_user.id,
            pic_file,
            caption=capt)


@bot.message_handler(commands=['start'])
def handle_start(m: Message):
    """Приветствие, регистрация"""
    uid = m.from_user.id
    check_user(uid, restart=True)
    global users
    # print(f"{m.text = }")

    show_random_picture(
        m, "start", 1, 3,
        "Мы очень неправильные глаголы!")

    bot.send_message(
        m.from_user.id,
        f"<b>Гутен таг, {m.from_user.first_name}!</b>\n\n"
        "Сегодня сдаём <b>неправильные английские глаголы</b>. Неожиданно?\n\n"
        "У тебя будет на выбор три персонажа и сложный путь подготовки "
        "к экзамену. Каждый твой ответ будет влиять на сюжет "
        "и на результат!\n\n"
        "Вот тут, например, <a href='https://www.native-english.ru/grammar/"
        "irregular-verbs'>можешь повторить глаголы</a> перед экзаменом.\n\n"
        "Подробнее - в справке /help\n"
        "<b>Начать игру - /play</b>",

        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=keyboard_main
    )


@bot.message_handler(
    content_types=["text"],
    func=lambda m: m.text == menu_main['play'])
@bot.message_handler(commands=['play'])
def handle_play(m: Message):
    """Принудительно запускаем новую игру"""
    uid = m.from_user.id
    check_user(uid, restart=True)
    global users
    # print(f"handle_play {m.text = }")

    # Пользователь нажал на один из rpg-классов. Показываем его картинку.
    if m.text in list(rpg_classes.values()):
        users[uid]['rpg_class'] = \
            [k for k, v in rpg_classes.items() if v == m.text][0]
        # {var_name = } is not compatible with 3.7
        # print(f"{uid = }, {users[uid]['rpg_class'] = }")

        show_random_picture(
            m, f"rpg_class_{users[uid]['rpg_class']}", 1, 4,
            "О, это будет круто!")

        # Гик ловкий. Для его предмета важно dexterity побольше
        if users[uid]['rpg_class'] == 'geek':
            users[uid]['p_hearing'] = randint(6, 8)
            users[uid]['p_vision'] = randint(6, 8)
            users[uid]['p_dexterity'] = randint(8, 11)
            users[uid]['p_logic'] = randint(4, 7)

        # Отличница зубрит на слух, и на глаз
        if users[uid]['rpg_class'] == 'nerd':
            users[uid]['p_hearing'] = randint(7, 11)
            users[uid]['p_vision'] = randint(6, 10)
            users[uid]['p_dexterity'] = randint(4, 7)
            users[uid]['p_logic'] = randint(7, 10)

        # Лентяй смышлёный, но ленивый ученик. Голова хорошо работает в стрессе.
        if users[uid]['rpg_class'] == 'idler':
            users[uid]['p_hearing'] = randint(5, 8)
            users[uid]['p_vision'] = randint(5, 8)
            users[uid]['p_dexterity'] = randint(6, 9)
            users[uid]['p_logic'] = randint(7, 12)

        normalize_rpg_params(uid)

        msg = bot.send_message(
            m.from_user.id,
            f"<b>{rpg_classes[users[uid]['rpg_class']]}</b> "
            f"- заявка на победу!\n\n"
            f"Великий бог RPG-рандома выдал тебе параметры:\n\n"
            f"Слух и слуховая память: "
            f"<b>{users[uid]['p_hearing']}</b> из 20\n"
            f"Зрение и зрительная память: "
            f"<b>{users[uid]['p_vision']}</b> из 20\n"
            f"Ловкость и мышечная память: "
            f"<b>{users[uid]['p_dexterity']}</b> из 20\n"
            f"Логическая память: "
            f"<b>{users[uid]['p_logic']}</b> из 20\n\n"
            f"Продолжаем?",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )
        # Переходим в первую локацию
        users[uid]['next_location'] = 'a'
        bot.register_next_step_handler(msg, handle_change_location)
        return

    show_random_picture(
        m, "select_char", 1, 4,
        "We all need to know irregular verbs!")

    keyboard_select_char = types.ReplyKeyboardMarkup(
        row_width=3,
        resize_keyboard=True
    )
    keyboard_select_char.add(*rpg_classes.values())

    # Делаем выбор персонажа, пока не выберет существующего.
    msg = bot.send_message(
        m.from_user.id,
        f"<b>Выбери персонажа!</b>\n\n"
        f"<b>ГИК</b> - повелитель гаджетов\n"
        f"<b>ОТЛИЧНИЦА</b> - мозг, как цепкий капкан\n"
        f"<b>ЛЕНТЯЙ</b> - великий прокрастинатор\n",

        parse_mode="HTML",
        reply_markup=keyboard_select_char
    )
    bot.register_next_step_handler(msg, handle_play)


def handle_change_location(m: Message):
    """Переходим между локациями"""
    uid = m.from_user.id
    check_user(uid)
    global users
    # print(f"{users[uid]['next_location'] = } {m.text = }")

    if users[uid]['next_location'] == 'a':
        teacher = choice(teacher_names)
        users[uid]['teacher_name'] = teacher

        msg = bot.send_message(
            m.from_user.id,
            f"Сегодня день экзамена по неправильным глаголам. "
            f"Тебя ждёт Самый Строгий Преподаватель - "
            f"<b>{users[uid]['teacher_name']}</b>!\n\n"
            f"Разумеется, <s>охота погулять</s> были дела и поважнее, "
            f"готовиться некогда... \n"
            f"Стыдно! Давай-ка поймём что к чему?",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )
        bot.register_next_step_handler(msg, handle_loc_a)

    if users[uid]['next_location'] == 'b':
        show_random_picture(
            m, "loc_b", 1, 4,
            "Кабинет химии. Час до экзамена.")

        msg = bot.send_message(
            m.from_user.id,
            "Ты с друзьями сидишь в кабинете химии. Как-то само собой "
            "разбились на группы и решили погонять по табличке: глагол на "
            "русском, а в ответ - три формы на английском.\n\n"
            f"С соседних пар слышно: <i>{choice(three_forms)}</i>... "
            "<i>Читать? Рид-Рэд-Рэд</i>...\n\n"
            "С тобой в паре Катя-Кэтрин-Кэт :) Давай штук 20 глаголов "
            "повторим? Если надоест, то можешь закончить после 10.",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )
        bot.register_next_step_handler(msg, handle_loc_b)

    if users[uid]['next_location'] == 'c':
        show_random_picture(
            m, "loc_c", 1, 4,
            "Кабинет английского. Несколько минут до экзамена.")

        msg = bot.send_message(
            m.from_user.id,
            "Ты сидишь в кабинете иностранного языка, ожидая "
            "своей очереди. Экзамен проходит прямо за этой стенкой. "
            "Иногда слышны шаги Проверяющих и резкий голос Самого Строгого "
            "Преподавателя: '<i>Вон из класса! Два!</i>'\n\n"
            f"{choice(spooky)} Зашёл твой друг {choice(friends)}, он уже сдал "
            f"экзамен. {choice(why)}\n\n"
            f"Говорит, что дают форму глагола на английском, "
            f"а ты должен написать другую форму. "
            f"Вы с Катей решили повторить тихонько именно так.",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )
        bot.register_next_step_handler(msg, handle_loc_c)

    if users[uid]['next_location'] == 'd':
        show_random_picture(
            m, "loc_d", 1, 4,
            "ЭКЗАМЕН! САМЫЙ СТРОГИЙ ПРЕПОДАВАТЕЛЬ!")

        msg = bot.send_message(
            m.from_user.id,
            "Ты входишь в экзаменационный зал.\n"
            "За партами сидят бледные ученики, "
            "между рядов рыскают старшеклассники - "
            "Проверяющие. Прямо в душу смотрит Самый Строгий "
            "Преподаватель. Её взгляд как будто высасывает радость "
            "и счастье...\n\n"
            "Внутренний голос: <i>Мне бы сейчас Экспекто патронум!</i>",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )
        bot.register_next_step_handler(msg, handle_loc_d)
    # return


""" aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa """


def handle_loc_a(m: Message):
    """Локация a - "Перед школой". Теоретические вопросы"""
    uid = m.from_user.id
    check_user(uid)
    global users
    # print(f"handle_loc_a {m.text = }")

    q_num = users[uid]['q_loc_a']

    # Если конец вопросов этой локации, то идём дальше.
    if users[uid]['q_loc_a'] == len(questions_a):
        normalize_rpg_params(uid)
        msg = bot.send_message(
            m.from_user.id,
            "Кстати, твои параметры изменились:\n\n"
            f"Слух и слуховая память: "
            f"<b>{users[uid]['p_hearing']}</b> из 20\n"
            f"Зрение и зрительная память: "
            f"<b>{users[uid]['p_vision']}</b> из 20\n"
            f"Ловкость и мышечная память: "
            f"<b>{users[uid]['p_dexterity']}</b> из 20\n"
            f"Логическая память: "
            f"<b>{users[uid]['p_logic']}</b> из 20\n\n",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )
        users[uid]['next_location'] = 'b'
        bot.register_next_step_handler(msg, handle_change_location)
        return

    # Если мы только зашли, то мини-опрос.
    if m.text != menu_continue['continue']:
        answers_q_num = questions_a[users[uid]['q_loc_a'] - 1]["a"]

        if m.text in answers_q_num:
            answer = answers_q_num[m.text]
            # print(f"{answer = }")
            users[uid]['p_hearing'] += answer[0]
            users[uid]['p_vision'] += answer[1]
            users[uid]['p_dexterity'] += answer[2]
            users[uid]['p_logic'] += answer[3]
            bot.reply_to(m, "Внутренний голос: " + answer[4])

    # В этой локации вопросы идут по порядку из словаря questions_a.
    # Варианты ответа перемешиваются.
    question = questions_a[q_num]
    markup_answers = types.ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True
    )
    a = list(map(str, question["a"].keys()))
    shuffle(a)
    markup_answers.add(* a)

    q_caption = "<b>Вопрос:</b>\n"
    if users[uid]['q_loc_a'] >= len(questions_a) - 1:
        q_caption = ""
    msg = bot.send_message(
        m.from_user.id,
        f"{q_caption}{question['q']}",

        parse_mode="HTML",
        reply_markup=markup_answers
    )
    users[uid]['q_loc_a'] += 1
    bot.register_next_step_handler(msg, handle_loc_a)


""" bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb """


def handle_loc_b(m: Message):
    """Локация b - "Кабинет химии". Теоретические вопросы"""
    uid = m.from_user.id
    check_user(uid)
    global users
    # print(f"handle_loc_b {m.text = }")

    # q_num = users[uid]['q_loc_b']

    # Если слишком много вопросов, то записываем rpg в БД и идём дальше.
    if users[uid]['q_num_b'] > 25 or m.text == 'Хватит':
        perc = 100 * users[uid]['q_num_b_ok'] // (users[uid]['q_num_b'] - 1)
        bot.send_message(
            m.from_user.id,
            "🤵‍♀️ <b>Катя:</b>\n<i>Наверное, хватит. Идём поближе "
            "к экзаменационному залу. Там ещё рядом кабинет английского "
            "есть. Там точно не пропустим начало.\n\n"
            f"Я прикинула: у тебя {perc}% правильных ответов.</i>",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )
        normalize_rpg_params(uid)
        msg = bot.send_message(
            m.from_user.id,
            "Кстати, твои параметры изменились:\n\n"
            f"Слух и слуховая память: "
            f"<b>{users[uid]['p_hearing']}</b> из 20\n"
            f"Зрение и зрительная память: "
            f"<b>{users[uid]['p_vision']}</b> из 20\n"
            f"Ловкость и мышечная память: "
            f"<b>{users[uid]['p_dexterity']}</b> из 20\n"
            f"Логическая память: "
            f"<b>{users[uid]['p_logic']}</b> из 20\n\n",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )
        users[uid]['next_location'] = 'c'
        bot.register_next_step_handler(msg, handle_change_location)
        return

    # Проверяем ответ на предыдущий вопрос, если попали сюда кнопкой Продолжить!
    # Если только зашли, то задаём первый вопрос.
    if m.text != menu_continue['continue']:
        answers_q_num = verbs[users[uid]['q_loc_b']]
        # print(f"{answers_q_num = }")

        # Если правильно ответил, то с некоторой вероятностью +параметры.
        # Считаем правильные ответы, чтобы потом не пустить на экзамен.
        correct_answer = ", ".join(answers_q_num[0:3])
        # mid = m.from_user.id
        if m.text == correct_answer:
            users[uid]['q_num_b_ok'] += 1
            bot.reply_to(
                m, f"<b>Кэт:</b>\n"
                   f"👍🏻 <i>{choice(right_answer)}</i>",
                parse_mode="HTML")
            if randint(0, 8) == 1:
                users[uid]['p_hearing'] += 1
                bot.send_message(
                    m.from_user.id, "♦️ Слух и слуховая память: +1")
            if randint(0, 8) == 1:
                users[uid]['p_vision'] += 1
                bot.send_message(
                    m.from_user.id, "♦️ Зрение и зрительная память: +1")
            if randint(0, 8) == 1:
                users[uid]['p_dexterity'] += 1
                bot.send_message(
                    m.from_user.id, "♦️ Ловкость и мышечная память: +1")
            if randint(0, 8) == 1:
                users[uid]['p_logic'] += 1
                bot.send_message(
                    m.from_user.id, "♦️ Логическая память: +1")
        # Если неправильно ответил,
        else:
            bot.reply_to(
                m, f"🤦🏼‍♀️ <b>Кэт:</b>\n"
                   f"<i>Нет. Правильно: {correct_answer}</i>",
                parse_mode="HTML")
            if randint(0, 9) == 1:
                users[uid]['p_hearing'] -= 1
                bot.send_message(
                    m.from_user.id, "⚡️ Слух и слуховая память: -1")
            if randint(0, 9) == 1:
                users[uid]['p_vision'] -= 1
                bot.send_message(
                    m.from_user.id, "⚡️ Зрение и зрительная память: -1")
            if randint(0, 9) == 1:
                users[uid]['p_dexterity'] -= 1
                bot.send_message(
                    m.from_user.id, "⚡️ Ловкость и мышечная память: -1")
            if randint(0, 9) == 1:
                users[uid]['p_logic'] -= 1
                bot.send_message(
                    m.from_user.id, "⚡️ Логическая память: -1")

    # В этой локации берём несколько случайных номеров глаголов из таблицы
    # Варианты ответа перемешиваются.
    rnd_verbs = [n for n in range(len(verbs))]
    shuffle(rnd_verbs)
    rnd_verbs = rnd_verbs[0:4]

    # Вопрос будет про первый случайный глагол, его номер запомним в q_loc_b.
    users[uid]['q_loc_b'] = rnd_verbs[0]
    verb = verbs[users[uid]['q_loc_b']]
    markup_answers = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )
    # Если достаточно много отвечал, то разрешаем выходить
    # Для отладки вместо 10 поставить 1, но потом вернуть 10!
    if users[uid]['q_num_b'] > 10:
        markup_answers.add('Хватит')

    # Берём из списка три формы глагола и объединяем в строку через запятую.
    a = []
    for i in range(4):
        a.append(verbs[rnd_verbs[i]][0:3])
    shuffle(a)
    b = [", ".join(x) for x in a]
    # print(f"{b = }")
    markup_answers.add(*b)

    msg = bot.send_message(
        m.from_user.id,
        "🤵‍♀️ <b>Кэт:</b>\n"
        f"<i>{verb[3]}</i>?",

        parse_mode="HTML",
        reply_markup=markup_answers
    )
    users[uid]['q_num_b'] += 1
    bot.register_next_step_handler(msg, handle_loc_b)


""" ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc """


def handle_loc_c(m: Message):
    """Локация c - "Кабинет английского". По одной форме назвать другую"""
    uid = m.from_user.id
    check_user(uid)
    global users
    # print(f"handle_loc_c {m.text = }")

    # Если слишком много вопросов, то записываем rpg в БД и идём дальше.
    if users[uid]['q_num_c'] > 25 or m.text == 'Хватит':
        perc = 100 * users[uid]['q_num_c_ok'] // (users[uid]['q_num_c'] - 1)
        bot.send_message(
            m.from_user.id,
            "🤵‍♀️ <b>Катя:</b>\n<i>"
            f"Ничего себе, {perc}% правильных ответов!\n"
            "Но, кажется, нас уже зовут. Побежали!</i>\n\n"
            "Схватили свои вещи и выбежали навстречу СУДЬБЕ! Если "
            "сдашь, то все дороги мира перед тобой открыты. Если не "
            "сдашь, то кричать 'Свободная касса' до конца времён...\n\n"
            "🖊 <b>Счастливая ручка осталась лежать на парте...</b>",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )

        normalize_rpg_params(uid)
        msg = bot.send_message(
            m.from_user.id,
            "Кстати, твои параметры изменились:\n\n"
            f"Слух и слуховая память: "
            f"<b>{users[uid]['p_hearing']}</b> из 20\n"
            f"Зрение и зрительная память: "
            f"<b>{users[uid]['p_vision']}</b> из 20\n"
            f"Ловкость и мышечная память: "
            f"<b>{users[uid]['p_dexterity']}</b> из 20\n"
            f"Логическая память: "
            f"<b>{users[uid]['p_logic']}</b> из 20\n\n",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )

        # Если все параметры ненулевые, то идём на экзамен.
        if (users[uid]['p_hearing']
                and users[uid]['p_vision']
                and users[uid]['p_dexterity']
                and users[uid]['p_logic']):
            users[uid]['next_location'] = 'd'
            bot.register_next_step_handler(msg, handle_change_location)
        # иначе ПРОИГРЫШ
        else:
            msg = bot.send_message(
                m.from_user.id,
                "<b>Память на нуле!</b>\n\n"
                f"Вся эта нервная обстановка, седой друг, ручка "
                f"счастливая потерялась где-то, каша в голове... "
                f"ты понимаешь, что на экзамене будет позор!\n\n"
                f"👨‍⚕️ В глазах начинает мутиться, ты теряешь сознание. "
                f"Следующий кадр - врач с нашатырём. Получив медотвод, "
                f"ты уныло бредёшь домой.",

                parse_mode="HTML",
                reply_markup=keyboard_shtosh
            )
            users[uid]['result'] = 'param_zero_fail'
            bot.register_next_step_handler(msg, handle_fail)
        return

    # Если мы только зашли, то задаём вопрос.
    # Если многовато вопросов, то предлагаем выйти.
    if m.text != menu_continue['continue']:
        answers_q_num = verbs[users[uid]['q_loc_c']]
        # print(f"{answers_q_num = }")

        # Если правильно ответил, то с некоторой вероятностью +параметры.
        # В этой локации и награждаем, и штрафуем сильнее.
        # Считаем правильные ответы, чтобы потом не пустить на экзамен.
        correct_answer = answers_q_num[users[uid]['q_loc_c_a']]
        full_answer = ", ".join(answers_q_num[0:3]) + " - " + answers_q_num[3]
        # print(f"{correct_answer =}")
        # mid = m.from_user.id
        if m.text.lower() == correct_answer:
            users[uid]['q_num_c_ok'] += 1
            bot.reply_to(
                m, f"<b>Кэт:</b>\n"
                   f"👍🏻 <i>{choice(right_answer)}</i>",
                parse_mode="HTML")
            if randint(0, 10) == 1:
                users[uid]['p_hearing'] += 2
                bot.send_message(
                    m.from_user.id, "♦️♦️ Слух и слуховая память: +2")
            if randint(0, 10) == 1:
                users[uid]['p_vision'] += 2
                bot.send_message(
                    m.from_user.id, "♦️♦️ Зрение и зрительная память: +2")
            if randint(0, 10) == 1:
                users[uid]['p_dexterity'] += 2
                bot.send_message(
                    m.from_user.id, "♦️♦️ Ловкость и мышечная память: +2")
            if randint(0, 10) == 1:
                users[uid]['p_logic'] += 2
                bot.send_message(
                    m.from_user.id, "♦️♦️ Логическая память: +2")
        # Если неправильно ответил,
        else:
            bot.reply_to(
                m, f"🤦🏼‍♀️ <b>Кэт:</b>\n"
                   f"<i>Нет. Должно быть <b>{correct_answer}</b>\n"
                   f"Вот все формы этого глагола:\n"
                   f"{full_answer}</i>",
                parse_mode="HTML")
            if randint(0, 12) == 1:
                users[uid]['p_hearing'] -= 2
                bot.send_message(
                    m.from_user.id, "⚡️⚡️ Слух и слуховая память: -2")
            if randint(0, 12) == 1:
                users[uid]['p_vision'] -= 2
                bot.send_message(
                    m.from_user.id, "⚡️⚡️ Зрение и зрительная память: -2")
            if randint(0, 12) == 1:
                users[uid]['p_dexterity'] -= 2
                bot.send_message(
                    m.from_user.id, "⚡️⚡️ Ловкость и мышечная память: -2")
            if randint(0, 12) == 1:
                users[uid]['p_logic'] -= 2
                bot.send_message(
                    m.from_user.id, "⚡️⚡️ Логическая память: -2")

    # Берём несколько случайных номеров глаголов из таблицы
    rnd_verbs = [n for n in range(len(verbs))]
    shuffle(rnd_verbs)
    rnd_verbs = rnd_verbs[0:4]

    # Вопрос будет про первый случайный глагол, его номер запомним в q_loc_c
    # а заданную и требуемую форму храним в users.
    users[uid]['q_loc_c'] = rnd_verbs[0]
    qa = [0, 1, 2]
    shuffle(qa)
    users[uid]['q_loc_c_q'] = qa[0]
    users[uid]['q_loc_c_a'] = qa[1]

    verb = verbs[users[uid]['q_loc_c']]
    markup_answers = types.ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True
    )
    markup_answers.add('Хватит')

    # Если достаточно много отвечал, то разрешаем выходить
    # Для отладки вместо 10 поставить 1, но потом вернуть 10!
    reply_markup_c = hideKeyboard
    if users[uid]['q_num_c'] > 10:
        reply_markup_c = markup_answers

    msg = bot.send_message(
        m.from_user.id,
        "🤵‍♀️ <b>Кэт:</b>\n"
        f"<i>У заданного глагола {users[uid]['q_loc_c_q'] + 1}-я форма: "
        f"<b>{verb[users[uid]['q_loc_c_q']]}</b>.\n"
        f"Какая у него {users[uid]['q_loc_c_a'] + 1}-я форма?</i>\n\n"
        f"(ответ напечатай)",

        parse_mode="HTML",
        reply_markup=reply_markup_c
    )
    users[uid]['q_num_c'] += 1
    bot.register_next_step_handler(msg, handle_loc_c)


""" ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd """


def handle_loc_d(m: Message):
    """Локация d - ЗКЗАМЕН! Подводим итоги!"""
    uid = m.from_user.id
    check_user(uid)
    global users
    # print(f"handle_loc_d {m.text = }")

    # Процент правильных ответов в твух форматах
    res_loc_b = 100 * users[uid]['q_num_b_ok'] // (users[uid]['q_num_b'] - 1)
    res_loc_c = 100 * users[uid]['q_num_c_ok'] // (users[uid]['q_num_c'] - 1)
    users[uid]['res_loc_b'] = res_loc_b
    users[uid]['res_loc_c'] = res_loc_c
    # {var_name = } is not compatible with 3.7
    # print(f"{users[uid]['q_num_b'] = }, {users[uid]['q_num_b_ok'] = }, "
    #       f"{users[uid]['q_num_c'] = }, {users[uid]['q_num_c_ok'] = }, "
    #       f"{res_loc_b = }, {res_loc_c = }")

    # Если отвечал наугад глаголы, то не пускать на экзамен
    if res_loc_b < 50 and res_loc_c < 50:
        msg = bot.send_message(
            m.from_user.id,
            "🙀 Внутренний голос: <i>Я НИЧЕГО НЕ ЗНАЮ!</i>\n\n"
            "Похлопав себя по карманам, ты понимаешь, что счастливая "
            "ручка потерялась! Но дело даже не в ручке...\n\n"
            "При повторе глаголов с Катей у тебя меньше половины правильных "
            f"ответов ({res_loc_b}% когда задано русское слово "
            f"и {res_loc_c}% когда задана английская форма). Кажется, "
            f"даже выбирая ответ монеткой, можно сдать экзамен лучше!\n\n"
            f"👨‍⚕️ В глазах начинает мутиться, ты теряешь сознание. "
            f"Следующий кадр - врач с нашатырём. Получив медотвод, "
            f"ты уныло бредёшь домой.",

            parse_mode="HTML",
            reply_markup=keyboard_shtosh
        )
        users[uid]['result'] = 'perc_low_fail'
        bot.register_next_step_handler(msg, handle_fail)
        return

    # Ловушка с именем-отчеством преподавателя
    # print(users[uid]['teacher_name'])
    answer_teachers = [users[uid]['teacher_name']]
    for i in range(5):
        a_teacher = choice(teacher_names)
        if a_teacher not in answer_teachers:
            answer_teachers.append(a_teacher)
        if len(answer_teachers) == 4:
            break

    markup_answers = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )
    shuffle(answer_teachers)
    markup_answers.add(*answer_teachers)

    bot.send_message(
        m.from_user.id,
        "<b>Преподаватель:</b>\n"
        f"<i>How are you today, <b>{m.from_user.first_name}</b>? Why are "
        f"you late? It's your duty to keep the blackboard clean!</i>\n\n"
        f"Ты в замешательстве от такого начала! И что там про доску?\n\n"
        f"На доске нарисована карикатура на преподавателя и снизу подпись: "
        f"<b>{choice(caricature)}</b>",

        parse_mode="HTML",
    )
    msg = bot.send_message(
        m.from_user.id,
        "<b>Ты:</b>\n"
        "<i>И-и-извините... Ай эм сорри... Ай эм окей тудэй... "
        "Я не знаю, кто это нарисовал! I do not know who painted it!</i>\n\n"
        f"По улыбкам других учеников ты понимаешь, что это был розыгрыш "
        f"преподавателя. Уууф! Кстати, надо поздороваться!\n\n"
        f"Good morning, ...",

        parse_mode="HTML",
        reply_markup=markup_answers
    )
    bot.register_next_step_handler(msg, handle_loc_d2)
    return


def handle_loc_d2(m: Message):
    """Проверяем, помнит ли имя-отчество преподавателя"""
    uid = m.from_user.id
    check_user(uid)
    global users
    # print(f"handle_loc_d2 {m.text = }")

    # Если не угадал учителя, то выгоняем с экзамена
    if m.text != users[uid]['teacher_name']:
        bot.send_message(
            m.from_user.id,
            f"<b>Преподаватель:</b>\n"
            f"<i>Wha-a-a-at?! I'm not {m.text}! "
            f"My name is {users[uid]['teacher_name']}! "
            f"Вон из класса! Два!</i>",

            parse_mode="HTML",
        )

        msg = bot.send_message(
            m.from_user.id,
            f"Ты рассеянно думаешь: 'Странно, ведь <i>Two</i>, "
            f"а не <i>Два</i>?'\n\n"
            f"Ээх, утром же повторяли и цвет учебника, и имя-отчество "
            f"преподавателя...\n\n"
            f"👨‍⚕️ В глазах начинает мутиться, ты теряешь сознание. "
            f"Следующий кадр - врач с нашатырём. Получив медотвод, "
            f"ты уныло бредёшь домой.",

            parse_mode="HTML",
            reply_markup=keyboard_shtosh
        )
        users[uid]['result'] = 'wrong_name_fail'
        bot.register_next_step_handler(msg, handle_fail)
        return
    # Если запомнил и правильно назвал преподавателя, то пускаем дальше.
    else:
        bot.send_message(
            m.from_user.id,
            f"<b>Преподаватель:</b>\n"
            f"<i>Спасибо, что не Эльза Букингемовна!</i>\n\n"
            f"Сидящие за партами ученики {choice(how)} захихикали по-"
            f"английски: <i>ha-ha-ha, he-he-he, ho-ho-ho, gy-gy-gy!</i>\n\n",

            parse_mode="HTML",
            reply_markup=keyboard_continue
        )

        # print(f"{rpg_items = } {users[uid]['rpg_class'] = }")
        msg = bot.send_message(
            m.from_user.id,
            f"Свободная парта у окна. Заполнив бланк, ты вспоминаешь о "
            f"домашней заготовке: "
            f"✨ <b>{rpg_items[users[uid]['rpg_class']]['name']}!</b>\n"
            f"{rpg_items[users[uid]['rpg_class']]['description']}\n\n"
            f"Рискнёшь воспользоваться? Успех зависит от твоих "
            f"параметров!",

            parse_mode="HTML",
            reply_markup=keyboard_yes_no
        )
        bot.register_next_step_handler(msg, handle_loc_d3)
        return


def handle_loc_d3(m: Message):
    """Использует или не использует RPG-предмет"""
    uid = m.from_user.id
    check_user(uid)
    global users
    # print(f"handle_loc_d3 {m.text = }")

    # выбираем ключевой параметр для разных классов:
    key_param = users[uid]['p_vision']
    if users[uid]['rpg_class'] == 'geek':
        key_param = users[uid]['p_dexterity']
    if users[uid]['rpg_class'] == 'nerd':
        key_param = max(users[uid]['p_hearing'], users[uid]['p_hearing'])
    if users[uid]['rpg_class'] == 'idler':
        key_param = users[uid]['p_logic']
    # print(f"{key_param = }")

    # Если согласен использовать RPG-предмет
    if m.text == menu_yes_no['yes']:
        # Делаем пометку, что предмет использовал.
        users[uid]['item_is_used'] = 1
        bot.send_message(
            m.from_user.id,
            f"👀 Сердце колотится, пальцы чуть дрожат от волнения... "
            f"Всё внимание уходит не на задание, а на попытку обмануть "
            f"Проверяющих...",
        )

        # По RPG-классике: кидаем dice d20. Если параметр >= d20, то успех!
        if key_param >= randint(1, 20):
            msg = bot.send_message(
                m.from_user.id,
                f"{rpg_items[users[uid]['rpg_class']]['success']}\n\n"
                f"{rpg_items['common']['success']}",

                parse_mode="HTML",
                reply_markup=keyboard_continue
            )
            users[uid]['result'] = 'item_win'
            bot.register_next_step_handler(msg, handle_win)
            return
        # ... Если параметр < d20, то fail!
        else:
            msg = bot.send_message(
                m.from_user.id,
                f"{rpg_items[users[uid]['rpg_class']]['fail']}",

                parse_mode="HTML",
                reply_markup=keyboard_shtosh
            )
            users[uid]['result'] = 'item_fail'
            bot.register_next_step_handler(msg, handle_fail)
            return

    # Если НЕ согласен использовать RPG-предмет.
    else:
        # Делаем пометку, что предмет не использовал.
        users[uid]['item_is_used'] = 0
        bot.send_message(
            m.from_user.id,
            f"👍🏻 Разумный выбор! Не хочется вылететь с экзамена без "
            f"права пересдачи. Сейчас вся надежда на твои параметры и на "
            f"подготовку с Катериной...",
        )

        # RPG-классика: кидаем dice d20. Если параметр >= d20, то успех.
        # Увеличим ключевой параметр за 100% тренировки с Катей.
        bonus_b = users[uid]['q_num_b_ok'] // (users[uid]['q_num_b'] - 1)
        bonus_c = users[uid]['q_num_c_ok'] // (users[uid]['q_num_c'] - 1)
        # print(f"{bonus_b = }, {bonus_c = }")

        # Для рандомного списка глаголов в следующей фразе.
        many_verbs = [z for x in verbs for z in x[0:2]]
        shuffle(many_verbs)
        many_many_verbs = ", ".join(many_verbs[0:100])

        if (key_param + bonus_b + bonus_c) >= randint(1, 20):

            msg = bot.send_message(
                m.from_user.id,
                f"Длинный список глаголов, как длинный питон: "
                f"<i>{many_many_verbs}</i>... \n\n"
                f"🤘🏻 А-а-а-а-а! И вот последняя точка! Стоило ли волноваться? "
                f"Все формы понятны, опечаток нет! Without a doubt, "
                f"this is a victory!",

                parse_mode="HTML",
                reply_markup=keyboard_continue
            )
            users[uid]['result'] = 'honestly_win'
            bot.register_next_step_handler(msg, handle_win)
            return
        # ... Если параметр < d20, то fail
        else:
            msg = bot.send_message(
                m.from_user.id,
                f"Грусть-тоска... Ты начинаешь считать ворон за окном. "
                f"Вот как тут можно понять что есть что: "
                f"<i>{many_many_verbs}</i>?!\n\n"
                f"Надо было готовиться лучше и выспаться. Знать имя-отчество "
                f"преподавателя недостаточно!",

                parse_mode="HTML",
                reply_markup=keyboard_shtosh
            )
            users[uid]['result'] = 'honestly_fail'
            bot.register_next_step_handler(msg, handle_fail)
            return


def handle_win(m: Message):
    """Окончательное сообщение об ошибке"""
    uid = m.from_user.id
    check_user(uid)
    global users
    global db_conn
    # print(f"handle_win {m.text = }")

    # Запись в таблицу результатов с пометкой Победа.
    insert_record(
        db_conn, int(time()),
        m.from_user.id, m.from_user.first_name,
        users[uid]
    )

    show_random_picture(
        m, "win", 1, 4,
        "ЭТО БЫЛО КРУТО!")

    bot.send_message(
        m.from_user.id,
        f"🌟 <b>ПОБЕДА! КВЕСТ УСПЕШНО ПРОЙДЕН!</b> 🌟\n\n"
        f"Прямо супер-пупер! Ты - мастер текстовых квестов! "
        f"И, несомненно, ты неплохо знаешь формы неправильных глаголов!\n\n"
        f"Теперь попробуй пройти за других персонажей или с другой "
        f"тактикой.\n\n"
        f"Или попробуй пройти оба обучения с Катей на 💯%, продержавшись "
        f"все 25 слов!",

        parse_mode="HTML",
        reply_markup=keyboard_main
    )


def handle_fail(m: Message):
    """Окончательное сообщение об ошибке"""
    uid = m.from_user.id
    check_user(uid)
    global users
    global db_conn
    # print(f"handle_fail {m.text = }")

    # Запись в таблицу результатов с пометкой Проигрыш.
    insert_record(
        db_conn, int(time()),
        m.from_user.id, m.from_user.first_name,
        users[uid]
    )

    show_random_picture(
        m, "fail", 1, 5,
        "Грустно и точка.")

    bot.send_message(
        m.from_user.id,
        f"☠️ <b>КВЕСТ ПРОВАЛЕН</b> ☠️\n\n"
        f"Верю: тебе по силам сдать экзамен. Выбери другого персонажа, "
        f"постарайся не повторять ошибок, соберись!\n\n"
        f"Иначе кричать тебе '🧑‍🍳 Свободная касса!' долгие годы, пока "
        f"искусственный интеллект не заменит тебя даже там.",

        parse_mode="HTML",
        reply_markup=keyboard_main
    )


@bot.message_handler(
    content_types=["text"],
    func=lambda m: m.text == menu_main['help'])
@bot.message_handler(commands=['help'])
def handle_help(m: Message):
    """Краткая справка"""
    # print(f"handle_help {m.text = }")

    bot.send_message(
        m.from_user.id,
        f"<b>Это бот-квест с элементами RPG для Яндекс.Практикума</b>\n\n"
        f"Представь себя школьником, которому сегодня сдавать "
        f"неправильные английские глаголы. Все твои действия имеют "
        f"значение!\n\n"
        f"Если невнимательно читаешь задания и не следишь за RPG-параметрами "
        f"персонажа, если глупо отвечаешь или просто не знаешь формы "
        f"неправильных глаголов, то экзамен ты ПРОВАЛИШЬ!\n\n"
        f"Попробуй пройти квест несколькими разными способами за разных "
        f"персонажей. Используй (или не используй) разные RPG-предметы. "
        f"Правильно отвечай, работая в паре с одноклассницей. "
        f"И тогда кроме удовольствия от победы ты неплохо прокачаешь свой "
        f"скил английского!\n\n"
        f"Играй много раз. Глаголы разные, их около 100. Скучно не будет!",

        parse_mode="HTML",
        reply_markup=keyboard_main
    )


# Скопипастил чужое решение для перехвата неуместных сообщений
CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video",
                 "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title",
                 "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created",
                 "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]


@bot.message_handler(content_types=CONTENT_TYPES)
def unknown_message(m: Message):
    """Перехват неуместных сообщений пользователя"""
    bot.send_message(
        m.from_user.id,
        f"Не понимаю тебя. Прочитай, что требуется ответить в квесте.",

        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=keyboard_main
    )


bot.polling(none_stop=True)
