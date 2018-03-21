import argparse
import random
import sys


def next_words(pair_of_all_words, curW):
    """Возращет следущее после cutWords слово(srt) которое надо
    вывести, либо кидает exception"""

    arr = [(i.split())[1] for i in pair_of_all_words if i.split()[0] == curW
           for j in range(int(i.split()[2]))]
    if len(arr) != 0:
        return random.choice(arr)
    else:
        # Если передали seed которого у нас нет
        return random.choice(pair_of_all_words)


def generate_text(model, seed, length, finalTextFile):
    'Метод генерирующий словосочетания, на основе модели'
    pair_of_all_words = model.readlines()
    if seed == '' or seed is None:
        seed = (random.choice(pair_of_all_words)).split()[0]

    curW = seed

    for i in range(length):
        finalTextFile.write(curW + ' ')
        curW = next_words(pair_of_all_words, curW)


parser = argparse.ArgumentParser(description='Cоставляет предложение')

parser.add_argument('--model', type=str, help='Путь для загрузки модели')
parser.add_argument('--seed', type=str, help='НЕОБЯАТЕЛЬНО! Начальное слово')
parser.add_argument('--length', type=int, help='Длина последовательности слов')
parser.add_argument('--output', default='', type=str, help='Вывод текста')

args = parser.parse_args()

with open(args.model, 'r') as file:
    if args.output == '':
        generate_text(file, args.seed, args.length, sys.stdout)
    else:
        with open(args.output, 'w') as output:
            generate_text(file, args.seed, args.length, output)
