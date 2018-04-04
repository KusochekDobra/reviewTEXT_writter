import collections
import argparse
import os
import re


def parse_str(s):
    'Парсит строку, выкидывая оттуда не алфавитные символы'
    return re.sub('[^a-zA-Zа-яА-Я]', '', s)




def to_lower(s):
    return ''.join(c for c in s.lower())


def give_last_word(s):
    if len(s.split()) > 0:
        return s.split()[-1]
    else:
        return ''


def give_first_word(s):
    return ''.join(re.findall(r'^\w+', s))


def filepath_to_good_shape(input_dir):
    """Функция возращает пути ко всем файлам-моделям"""
    path_f = []
    for d, dirs, files in os.walk(input_dir):
        for f in files:  # Считываем только txt файлы
            if f[-4:] == '.txt':
                path = os.path.join(d, f)  # формирование адреса
                path_f.append(path)  # добавление адреса в список
    return path_f


def generate_words(input_dir, out, lc):
    c = collections.Counter()
    for fileName in input_dir:
        with open(fileName, 'r', encoding="utf8") as file:
            line = parse_str(file.readline())

            while line:
                if len(line) > 0:
                    if lc:
                        line = line.lower()

                    for i in [' '.join([i for i
                                        in (line.split())][j:j + 2])
                              for j in range(len(line.split()) - 1)]:
                        c[i] += 1

                last_word = give_last_word(line)

                line = parse_str(file.readline())
                first_word = give_first_word(line)

                if first_word != '' and last_word != '':
                    if lc:
                        last_word = last_word.lower()
                        first_word = first_word.lower()

                    c[parse_str((last_word + ' ' + first_word))] += 1

    if out != '':
        with open(out, 'w', encoding="utf8") as output:
            for i in c:
                print('{} {}'.format(i, c[i]), file=output)
    else:
        print('{} {}'.format(i, c[i]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--model',
                        type=str, help='Путь к файлу,'
                                       ' в который загружается модель')
    parser.add_argument('--lc', default=False,
                        action='store_true', help='')
    parser.add_argument('--input-dir', default='',
                        type=str, help='Дериктория текстов для обучения'
                                       '!ТОЛЬКО txt ФАЙЛЫ!')

    args = parser.parse_args()
    if args.input_dir == '':

        with open('additional_input', 'w', encoding="utf8") as add_input:
            line = input()
            while line != '':
                add_input.write(line + '\n')
                line = input()
        generate_words(['additional_input'], args.model, args.lc)
    else:
        generate_words(filepath_to_good_shape(args.input_dir),
                       args.model, args.lc)

    print(' "{}" generation is completed successfully'.format(args.model))
