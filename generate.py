"""
Скрипт создаёт текст на основе модели, которую вы создали
с помощью {train.py} и указанной вами длины - length.
!Причем все синтаксические средства опускаются!

Особенности программы(кратко):
Для того чтобы подобрать слово следующее слово:
    а) Состовляем массив из всех слов которые идут после
текущего умноженного на соответстующую частоту
    б) random.choice'ом выбираем какое слово должно идти
после текущего

Пример:
model: а б - 2,  а в - 2
Массив из которого будет выбираться случ. слово:
{б, б, в, в}

@author: Подкидышев Алексей
@email: alexp2019@gmail.com
"""

import argparse
import random
import sys
import json


def next_words(dic_of_all_words, cur_w):
    """
    Находит следующее после cur_w слово


    :param dic_of_all_words: все пары слов и частоты,
    хранимые в списке
    :param  cur_w: текущее слово

    :return: следущее слово
    :raise: ValueError, если подано несущесвтующее
                    начальное слово
    """

    for i in dic_of_all_words.keys():
        if i == cur_w:
            helps_array = list(dic_of_all_words[i])
            [helps_array.append(j) for j in dic_of_all_words[i]
             for k in range(dic_of_all_words[i][j])]
            return random.choice(helps_array)

    if cur_w == args.seed:
        raise ValueError('seed does not exist')
    # Если след. слова нет в модели, генерируем случайное

    return str(random.choice(list(dic_of_all_words)))
    # exit(256)


def generate_text(model, seed, length, finalTextFile):
    'Метод генерирующий словосочетания, на основе модели'

    dic_of_all_words = dict(json.load(model))

    if seed == '' or seed is None:
        seed = (random.choice(list(dic_of_all_words.keys())))

    cur_w = seed

    for i in range(length):
        finalTextFile.write(cur_w + ' ')
        cur_w = next_words(dic_of_all_words, cur_w)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Cоставляет текст на основе модели')

    parser.add_argument('--model', type=str,
                        help='Путь для загрузки модели',
                        required=True)
    parser.add_argument('--seed', type=str,
                        help='Начальное слово')
    parser.add_argument('--length', type=int, required=True,
                        help='Длина'
                             ' последовательности слов')
    parser.add_argument('--output', default='sys.stdout', type=str,
                        help='Вывод текста')

    args = parser.parse_args()

    with open(args.model, 'r', encoding="utf8") as file:
        if args.output == 'sys.stdout':
            generate_text(file, args.seed, args.length, sys.stdout)
        else:
            with open(args.output, 'w', encoding="utf8") as output:
                generate_text(file, args.seed, args.length, output)

    print('\n')
    print(' "{}" TEXT generation is'
          ' completed successfully'.format(args.output))
