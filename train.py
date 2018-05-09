"""
Скрипт создаёт модель на основе текстов которые вы ему передали
В ней("your_model_name".txt) отражено как часто за i словом следует j-ое:
      Формат : СЛОВО1 _ СЛОВО2 _ кол-во

Особенности программы(кратко):
1) Для парсинга строки и получения последнего/первого слова
    используем библиотеку re
2) Кодировка UTF-8
3) Для подсчета частоты пар используем collections.Counter

@author: Подкидышев Алексей
@email: alexp2019@gmail.com
"""

import collections
import argparse
import os
import re
import sys
import json
from collections import defaultdict


def parse_str(s, parse_const):
    'Парсит строку, выкидывая оттуда не алфавитные символы'
    if parse_const == 0:
        return re.sub('[^a-zA-Zа-яА-Я]', ' ', s)
    if parse_const == 1:
        return re.sub('[^a-zA-Zа-яА-Я ]', '', s).replace(',', ' ')


def give_last_word(s):
    return s.rsplit(None, 1)[-1]


def file_path_to_good_shape(input_dir):
    """
    Функция ищет все файлы в директории

    Keyword arguments:
    :param input_dir: Директория в котором лежат файлы для
    обучения
    :return path_f: список имен файлов
    """
    path_files = []
    [path_files.append(os.path.join(first_tuple_element, cur_file))
     for first_tuple_element, dirs, files
     in os.walk(input_dir) for cur_file in files]
    return path_files


def crate_dic_from_Counter(counter):
    res_dict = defaultdict(lambda: defaultdict(int))

    for (word1, word2), num in counter.items():
        res_dict[word1][word2] = num
    return res_dict


def generate_words(file, lc):
    """
    Функция генерирует модель(Записывает Counter в файл
    при помощи библиотеки json)

    :param file, lc: файл из которого считываем пары,
    нужно ли приводить строку к lc
    :return counter: counter содержащий пары слов и их частоту
    повторений в тексте
    """

    counter = collections.Counter()
    counter[0, 0] = 0
    last_word = ''
    for line in file:
        line = last_word + parse_str(line, 0)
        if len(line) > 0:
            if lc:
                line = line.lower()

        counter.update(zip(str(line[:-1]).replace(' ', ''),
                           str(line[1:]).replace(' ', '')))
        last_word = give_last_word(line)

        if lc:
            last_word = last_word.lower()

    return counter


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--model',
                        type=str, help='Путь к файлу,'
                                       ' в который загружается модель',
                        required=True)
    parser.add_argument('--lc', default=False,
                        action='store_true', help='')
    parser.add_argument('--input-dir', default='',
                        type=str, help='Дериктория текстов для обучения')

    args = parser.parse_args()
    counter = collections.Counter()

    if args.input_dir == '':
        # Для того, чтобы оставновить ввод, комбинация CTRL + Z
        counter += generate_words(sys.stdin, args.lc)
    else:
        for i in file_path_to_good_shape(args.input_dir):
            print(i)
            with open(i, 'r', encoding="utf8") as file:
                counter += generate_words(file, args.lc)

    out = args.model
    if out != '':
        with open(out, 'w', encoding='utf-8') as file:
            print(crate_dic_from_Counter(counter))
            json.dump(crate_dic_from_Counter(counter), file)

    print(' "{}" generation is completed successfully'.format(args.model))
