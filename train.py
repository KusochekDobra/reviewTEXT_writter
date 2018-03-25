import collections
import argparse
import os
import sys
import re


# coding: utf-8


def parse_str(s):
    'Парсит строку, выкидывая оттуда не алфавитные символы'
    return re.sub('[–!—@#$:`€1234567890;()»%^+=?*[\].\n/,\-\"\r\']', ' ', s)


def to_lower(s):
    return ''.join(c for c in s.lower())


def give_last_word(s):
    return ''.join(re.findall(r'\w+$', s))


def give_first_word(s):
    return ''.join(re.findall(r'^\w+', s))


def filepath_to_input_shape(input_dir):
    """Функция возращает пути ко всем файлам-моделям"""
    path_f = []
    for d, dirs, files in os.walk(input_dir):
        for f in files:
            if str(f).startswith('TextLearning'):
                path = os.path.join(d, f)  # формирование адреса
                path_f.append(path)  # добавление адреса в список
    return path_f


def generate_words(input_dir, out, lc):
    c = collections.Counter()
    for fileName in input_dir:
        with open(fileName, 'r') as file:
            line = parse_str(file.readline())

            while line:
                if line != '\n':

                    if len(line) > 1:
                        if lc:
                            line = line.lower()

                        for i in [' '.join([i for i
                                            in (line.split())][j:j + 2])
                                  for j in range(len(line.split()) - 1)]:
                            c[i] += 1

                    last_word = parse_str(give_last_word(line))
                    if lc:
                        last_word = last_word.lower()

                line = parse_str(file.readline())
                first_word = parse_str(give_first_word(line))
                if lc:
                    first_word = first_word.lower()
                if first_word != '' and last_word != '':
                    c[parse_str((last_word + ' ' + first_word))] += 1

    if out != '':
        with open(out, 'w') as output:
            for i in c:
                print('{} {}'.format(i, c[i]), file=output)
    else:
        print('{} {}'.format(i, c[i]))


# _________________________________________MAIN________________________________________________
parser = argparse.ArgumentParser()

parser.add_argument('--model', default='mater\output.txt',
                    type=str, help='Путь к файлу в который загружается модель')
parser.add_argument('--lc', default=False,
                    action='store_true', help='К нижнему подчеркиванию')
parser.add_argument('--input_dir', default='',
                    type=str, help='Дериктория текстов для обучения')

args = parser.parse_args()
if args.input_dir == '':
    generate_words(sys.stdin, args.model, args.lc)
else:
    generate_words(filepath_to_input_shape(os.getcwd() + '\\' + args.input_dir), args.model, args.lc)
