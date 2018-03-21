import collections
import string
import random
from random import uniform
from collections import defaultdict
import re


def next_words(pair_of_all_words, curW):
    'Возращет следущее после cutWords слово(srt) которое надо вывести, либо кидает exception'
    print(curW)
    arr = [(i.split())[1] for i in pair_of_all_words if i.split()[0] == curW for j in range(int(i.split()[2]))]
    print(arr)
    if len(arr) != 0:
        return random.choice(arr)


print(next_words(['Спасибо что 4\n'
                  'что скачали 4\n'
                  'скачали книгу 4\n'
                  'книгу в 4\n',
                  'в бесплатной 4\n',
                  'бесплатной электронной 4\n'
                  'электронной библиотеке 4\n'], 'что'))
