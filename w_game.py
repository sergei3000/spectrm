from collections import defaultdict
from copy import deepcopy


# - прочитать весь файл в список
with open('wg.txt') as file:
    allWords = file.readlines()
allWords = [word.strip() for word in allWords]
# - из списка сделать словарь
allWordsDict = defaultdict(set)
for word in allWords:
    allWordsDict[word[0]].add(word.lower())
# - сделать копию словаря
onHand = deepcopy(allWordsDict)
# - переменная для использованных слов
usedWords = []
# - переменная новых слов
newWords = []
# - переменная окончания игры конецигры=ложь
endGame = False
# - переменная последней буквы
lastChar = ''
# Разрешённые буквы
rusLetters = [chr(c) for c in range(ord('а'), ord('я')+1)] + ['ё']

# - функция игры компьютера
# - функция игры человека
# -игра


# **Функция последней буквы (слово)
# если последняя буква в "ьъы" то вернуть предпоследнюю
# иначе вернуть последнюю
def lastCharFunc(word):
    if word[-1] in 'ьъыЬЪЫ':
        return word[-2].lower()
    return word[-1].lower()

# **Функция компьютера(последняя буква)**
def computer(char):
    # -- ЕСЛИ ЕСТЬ слово на последнюю букву, то последняя буква = функция последней буквы этого слова
    # - и удалить слово из копии словаря
    if len(onHand[char]) > 0:
        wordPick = onHand[char].pop()
        print('Выбор компьютера:', wordPick)
        last = lastCharFunc(wordPick)
        # - добавить слово к использованным
        usedWords.append(wordPick)
        return (False, last)
    # -- иначе конецигры = (истина, "ты победил")
    else:
        # вернуть конец игры
        return (True, None)

# **Функция человека(последняя буква)**
def human(char):

    while True:
        # - Запрос слова
        humanWord = input('Введите слово на букву {} или "сдаюсь": '.format(char)).lower()
        humanWord = humanWord.replace('ё', 'е')
        # - Если "сдаюсь", endgame = (True, "Computer wins!"), break
        if humanWord == 'сдаюсь':
            result = (True, None)
            break

        # Иначе проверка символов (русский алфавит) и начало цикла ввода
        #print(any([letter not in rusLetters for letter in humanWord]))
        elif any([letter not in rusLetters for letter in humanWord]):
            print('Разрешены только буквы и только кириллица. Попробуйте ещё раз.')
            continue

        # иначе проверка буквы(цикл) и принт
        elif humanWord[0] != char:
            print("Не та буква. Введите слово на букву {}.".format(char))
            continue

        # - Иначе:если уже было - "Введите снова!"
        elif humanWord in usedWords:
            print("Уже было. Введите другое слово.")
            continue

        # Проверка - есть ли такое слово
        elif humanWord not in allWords:
            print("Нет такого слова. Попробуйте ещё раз.")
            continue

        # Иначе ок, принимается
        else:
            print('OK!')
            # - добавить к использованным
            usedWords.append(humanWord)
            # - если слово есть в копии словаря, удалить из копии словаря иначе добавить в новые слова
            if humanWord in onHand[humanWord[0]]:
                onHand[humanWord[0]].remove(humanWord)
            else:
                newWords.append(humanWord)
            # - последняя буква = функция последней буквы посл.бук.
            last = lastCharFunc(humanWord)
            result = (False, last)
            break
    return result


# *** ИГРА
#
# - первый ввод
while True:
    firstWord = input('Введите слово (нарицательное существительное'
                      ' в единственном числе и именительном падеже): ').lower()
    firstWord = firstWord.replace('ё', 'е')
    if any([letter not in rusLetters for letter in firstWord]):
        print('Разрешены только буквы и только кириллица. Попробуйте ещё раз.')
        continue
    elif firstWord not in allWords:
        print("Нет такого слова. Попробуйте ещё раз.")
        continue
    elif firstWord in onHand[firstWord[0]]:
        onHand[firstWord[0]].remove(firstWord)
    else:
        newWords.append(firstWord)
    usedWords.append(firstWord)
    lastChar = lastCharFunc(firstWord)
    print('OK!')
    break

# **Цикл игры
while True:
    # -функция компьютера()
    endGame, lastChar = computer(lastChar)
    # - если конецигры то брэйк
    if endGame:
        print('You win!')
        break

    # -функция человека()
    endGame, lastChar = human(lastChar)
    # -если конец игры то брэйк
    if endGame:
        print('Computer wins!')
        break

# - обновить словарь
for word in newWords:
    allWordsDict[word[0]].add(word)
# - сохранить новый словарь
with open('updated.txt','w') as file:
    for words in allWordsDict.values():
        for word in words:
            file.write('{}\n'.format(word))
# - напечатать конец игры
print('Game over')