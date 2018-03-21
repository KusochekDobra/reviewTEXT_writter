import string
import collections
import argparse
import os
import sys
import re


def parse_str(s):
    'Парсит строку'
    return re.sub('[!—@#$:()%^+=?*[\].\n/,]', ' ', s)


def to_lower(s):
    return ''.join(c for c in s.lower())


def give_last_word(s):
    return ''.join(re.findall(r'\w+$', s))


def give_first_word(s):
    return ''.join(re.findall(r'^\w+', s))


def generate_words(input_dir, out, lc):
    c = collections.Counter()

    for fileName in input_dir:
        if fileName[:2] == 'in':
            with open('mater/' + fileName, 'r') as file:
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
parser = argparse.ArgumentParser(description='Укажите необхожимый параметр')

parser.add_argument('--model', type=str, help='Путь к файлу'
                                              'в который загружается модель')
parser.add_argument('--lc', action='store_true', help='lower_case')
parser.add_argument('--input_dir', type=str, help='Пути тексто в для обучения')

args = parser.parse_args()
if args.input_dir == '':
    generate_words(sys.stdin, args.model, args.lc)
else:
    generate_words(os.listdir(args.input_dir), args.model, args.lc)
