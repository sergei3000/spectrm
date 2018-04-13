# -*- coding: utf-8 -*-
import config
import telebot
from collections import defaultdict
from copy import deepcopy
from datetime import date
from time import sleep
from threading import Thread

bot = telebot.TeleBot(config.token)

# Прочитать весь файл в список
with open('wg.txt') as file:
    all_words = file.readlines()
all_words = [word.strip() for word in all_words]
# Из списка сделать словарь
all_words_dict = defaultdict(set)
for word in all_words:
    all_words_dict[word[0]].add(word.lower())
# Разрешённые буквы
rus_letters = [chr(c) for c in range(ord('а'), ord('я') + 1)] + ['ё']
# Игроки и даты их последнего валидного сообщения
players = {}


# Определение последней буквы
def last_char_func(word):
    if word[-1].lower() in 'ьъы':
        return word[-2].lower()
    return word[-1].lower()


# Проверка слова на правильные буквы
def check_letters(word):
    for char in word:
        if char not in rus_letters:
            return False
    return True


class WordsGame(object):
    def __init__(self):
        # Сделать копию словаря
        self.on_hand = deepcopy(all_words_dict)
        # Переменная для использованных слов
        self.used_words = []
        # Переменная новых слов (может понадобиться)
        self.new_words = []
        # Переменная последней буквы (меняется только ботом)
        self.last_char = ''

    # **Функция компьютера(последняя буква)**
    def bot_move(self, char):
        '''Метод хода бота
        Возвращает метку конца игры'''
        # Если есть слово на последнюю букву, то последняя буква = функция последней буквы этого слова
        # И удалить слово из копии словаря
        if len(self.on_hand[char]) > 0:
            word_pick = self.on_hand[char].pop()
            # Меняем последнюю букву
            self.last_char = last_char_func(word_pick)
            # Добавить слово к использованным
            self.used_words.append(word_pick)
            #print('Выбор компьютера:', word_pick)
            return False, word_pick
        # Иначе конецигры = (истина, "ты победил")
        else:
            # вернуть конец игры
            return True, None


@bot.message_handler(commands=['start'])
def handle_start(message):
    players[message.chat.id] = {'object': WordsGame(), 'date': date.today()}
    bot.send_message(message.chat.id, 'Введите слово (существительное в '
                                      'именительном падеже и единственном числе).')


@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_message(message):
    human_word = message.text.lower()
    human_word = human_word.replace('ё', 'е')
    id = message.chat.id
    if id in players:
        player = players[id]['object']
    if id not in players:
        bot.send_message(id, 'Чтобы начать игру, отправьте /start')
    elif human_word == 'сдаюсь':
        del players[id]
        bot.send_message(id, 'Игра окончена. Чтобы сыграть ещё раз, отправьте /start.')
    elif not check_letters(human_word):
        bot.send_message(id, 'Разрешены только буквы и только кириллица. Попробуйте ещё раз.')
    elif human_word[0] != player.last_char and player.last_char != '':
        bot.send_message(id, 'Не та буква. Отправьте слово на букву {}.'.format(player.last_char))
    elif human_word in player.used_words:
        bot.send_message(id, 'Уже было. Пришлите другое слово.')
    elif human_word not in all_words:
        bot.send_message(id, 'Нет такого слова. Попробуйте ещё раз.')
    else:
        players[id]['date'] = date.today()
        first = human_word[0]
        last = last_char_func(human_word)
        player.used_words.append(human_word)
        # с if - для задела на будущее (ввод уровней сложности)
        # по-простому можно без условия просто удалить слово
        if human_word in player.on_hand[first]:
            player.on_hand[first].remove(human_word)
        # Результат игры бота - (метка проигрыша, слово бота)
        bot_result = player.bot_move(last)
        if bot_result[0]:
            del players[id]
            bot.send_message(id, 'Поздравляю! Вы победили!'
                                 'Чтобы сыграть ещё раз, отправьте /start')
        else:
            bot.send_message(id, 'Мой ход: "{}". Отправьте слово на букву "{}". '
                                 'Если сдаётесь, отправьте "сдаюсь".'
                             .format(bot_result[1], last_char_func(bot_result[1])))


# Удаление неактивных игроков
def check_activity(players):
    while True:
        for p in players:
            if (date.today() - players[p]['date']).days > 1:
                del players[p]
        sleep(3600)


t2 = Thread(target=check_activity, args=(players,))
t2.start()


if __name__ == '__main__':
    bot.polling(none_stop=True)
