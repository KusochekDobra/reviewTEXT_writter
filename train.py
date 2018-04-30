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


def parse_str(s):
    'Парсит строку, выкидывая оттуда не алфавитные символы'
    return re.sub('[^a-zA-Zа-яА-Я]', ' ', s)


def give_last_word(s):
    return ''.join(re.findall(r'\w+$', s))


def give_first_word(s):
    return ''.join(re.findall(r'^\w+', s))


def file_path_to_good_shape(input_dir):
    'Функция возращает пути ко всем файлам-моделям'
    path_f = []
    [path_f.append(os.path.join(first_tuple_element, cur_file))
     for first_tuple_element, dirs, files
     in os.walk(input_dir) for cur_file in files]
    return path_f


def generate_words(file, lc):
    counter = collections.Counter()
    line = parse_str(file.readline())

    while line:
        if len(line) > 0:
            if lc:
                line = ''.join(c for c in line.lower())

        allWords = line.split()
        counter += collections.Counter([' '.join([i for i in allWords]
                                                 [j:j + 2])
                                        for j in range(
                len(allWords) - 1)])

        last_word = give_last_word(line)

        line = parse_str(file.readline())
        first_word = give_first_word(line)

        if first_word != '' and last_word != '':
            if lc:
                last_word = last_word.lower()
                first_word = first_word.lower()

            counter[parse_str((last_word + ' ' + first_word))] += 1

    return counter


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--model',
                        type=str, help='Путь к файлу,'
                                       ' в который загружается модель')
    parser.add_argument('--lc', default=False,
                        action='store_true', help='')
    parser.add_argument('--input-dir', default='',
                        type=str, help='Дериктория текстов для обучения')

    args = parser.parse_args()
    counter = collections.Counter()

    if args.input_dir == '':
        # Для того, чтобы оставновить ввод, тыкаейте CTRL + Z
        counter += generate_words(sys.stdin, args.lc)
    else:
        for i in file_path_to_good_shape(args.input_dir):
            print(i)
            with open(i, 'r', encoding="utf8") as file:
                counter += generate_words(file, args.lc)

    out = args.model

    if out != '':
        with open(out, 'w', encoding="utf8") as output:
            for i in counter:
                print('{} {}'.format(i, counter[i]), file=output)
    else:
        for i in counter:
            print('{} {}'.format(i, counter[i]))

    print(' "{}" generation is completed successfully'.format(args.model))
