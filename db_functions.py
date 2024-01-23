#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""2024-01-12 Fil - Future code Yandex.Practicum
Бот-квест "Экзамен по неправильным английским глаголам"
Описание в README.md

Вынес в модуль некоторые функции с базой данных
"""

import sqlite3


# Создаем таблицу для хранения статистики законченных игр
def create_tables(the_db_conn):
    the_dbc = the_db_conn.cursor()
    try:
        the_dbc.execute(
            'CREATE TABLE IF NOT EXISTS Finished_Games ('
            'id INTEGER PRIMARY KEY, '
            'user_id INTEGER, '
            'user_name TEXT, '
            'time_finished INTEGER, '
            'rpg_class INTEGER, '
            'p_hearing INTEGER, '
            'p_vision INTEGER, '
            'p_dexterity INTEGER, '
            'p_logic INTEGER, '
            'item_is_used INTEGER, '
            'success INTEGER'
            ')'
        )
        the_db_conn.commit()
        print(f"Создал таблицу хранения результатов Finished_Games.")
    except sqlite3.Error:
        print("Ошибка при создании таблицы хранения результатов.")


# Создаем таблицу для хранения статистики законченных игр
def insert_record(the_db_conn, the_time: int,
                  user_id: int, user_name: str,
                  user: list, res: int):
    the_dbc = the_db_conn.cursor()
    data = [user_id, user_name,
            the_time, user["rpg_class"],
            user["p_hearing"], user["p_vision"],
            user["p_dexterity"], user["p_logic"],
            user["item_is_used"], res
            ]
    try:
        the_dbc.execute("INSERT INTO Finished_Games "
                    "("
                    "user_id, user_name, "
                    "time_finished, rpg_class, "
                    "p_hearing, p_vision, "
                    "p_dexterity, p_logic, "
                    "item_is_used, success "
                    ") "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        data
                    ))
        the_db_conn.commit()
        print(f"Добавил запись о законченной игре (Квест провален).")
    except sqlite3.Error:
        print("Ошибка при добавлении записи о законченной игре.")
