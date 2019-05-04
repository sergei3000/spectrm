# -*- coding: utf-8 -*-
from collections import defaultdict
from copy import deepcopy
from datetime import date
from threading import Thread
from time import sleep

import telebot

import config


bot = telebot.TeleBot(config.token)

# Read words file into a list
with open('wg.txt') as file:
    all_words = file.readlines()
all_words = [word.strip() for word in all_words]
# Turn list into dictionary
all_words_dict = defaultdict(set)
for word in all_words:
    all_words_dict[word[0]].add(word.lower())
# Acceptable characters
rus_letters = [chr(c) for c in range(ord('а'), ord('я') + 1)] + ['ё']
# Players together with dates of their last valid message
players = {}


# Getting the last letter of the word
def last_char_func(word):
    if word[-1].lower() in 'ьъы':
        return word[-2].lower()
    return word[-1].lower()


# Check the word's letters for correctness
def check_letters(word):
    for char in word:
        if char not in rus_letters:
            return False
    return True


class WordsGame(object):
    def __init__(self):
        # Make a copy of the dictionary with all words
        self.on_hand = deepcopy(all_words_dict)
        # Variable for words already used in the game
        self.used_words = []
        # Variable for new words (might need it in future)
        self.new_words = []
        # Last letter variable (can only be changed by bot)
        self.last_char = ''

    # Bot's method (last letter)
    def bot_move(self, char):
        '''Bot's move method
        Returns True if bot loses and game is over
        Returns False and bot's word otherwise'''
        # If bot finds a word starting with the current last letter
        # the last letter becomes = last_char function of bot's word
        # And this word is deleted from the dictionary
        if len(self.on_hand[char]) > 0:
            word_pick = self.on_hand[char].pop()
            # Change the last letter
            self.last_char = last_char_func(word_pick)
            # Add word to used ones
            self.used_words.append(word_pick)
            #print('Выбор компьютера:', word_pick)
            return False, word_pick
        # Else end of game = (True, "you win")
        else:
            # return end of game
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
        # next 'if' might be needed in future (to introduce difficulty levels)
        # without this requirement the word can be deleted unconditionally
        if human_word in player.on_hand[first]:
            player.on_hand[first].remove(human_word)
        # Result of bot's move - (loss message or bot's word)
        bot_result = player.bot_move(last)
        if bot_result[0]:
            del players[id]
            bot.send_message(id, 'Поздравляю! Вы победили!'
                                 'Чтобы сыграть ещё раз, отправьте /start')
        else:
            bot.send_message(id, 'Мой ход: "{}". Отправьте слово на букву "{}". '
                                 'Если сдаётесь, отправьте "сдаюсь".'
                             .format(bot_result[1], last_char_func(bot_result[1])))


# Delete inactive players
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
