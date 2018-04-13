# -*- coding: utf-8 -*-
import config
import telebot
from collections import defaultdict
from copy import deepcopy
from datetime import date
from time import sleep
from threading import Thread
import psycopg2  # Импортируем библиотеку


# Устанавливаем соединение
conn = psycopg2.connect(
    dbname="wgame",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
cur = conn.cursor()  # Берем курсор


# bot = telebot.TeleBot(config.token)


# Прочитать все слова из базы в список
cur.execute("SELECT word FROM words_table;")  # “Выбираем” все слова в таблице
data = cur.fetchall()
all_words = [item[0] for item in data]

cur.close()  # Закрываем курсор
conn.close()  # Закрываем соединение


print(len(all_words))
print(type(all_words))
print(all_words[:5])
print(all_words[-5:])

