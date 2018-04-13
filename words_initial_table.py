# --Скрипт запускается один раз, для создания таблицы со словами в базе--

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

# Создаем таблицу words_table
cur.execute("CREATE TABLE words_table (id serial PRIMARY KEY, word varchar);")

# Добавляем данные в таблицу
# Прочитать весь файл в список
with open('wg.txt') as file:
    all_words = file.readlines()
all_words = [word.strip() for word in all_words]
# Команда для переноса слов в базу
print(len(all_words))
print(all_words[0])
print(all_words[-1])
for num, word in enumerate(all_words):
    cur.execute("INSERT INTO words_table (id, word) VALUES (%s, %s)", (num, word))

conn.commit()  # Сохраняем информацию в БД
cur.close()  # Закрываем курсор
conn.close()  # Закрываем соединение

