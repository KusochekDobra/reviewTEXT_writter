# Генератор текстов
[Задание](https://docs.google.com/document/d/1ka4MdenzgrdfXiyOU_HxEjjXPhehNk-yWX7K2h3zdkI/edit)

## Как это работает?
1. Сначала запускаем python train.py  
--input_dir _Имя_директории_(где находяться файлы. Файлы **должны начинаться с in**)  
--model Имя_файла  
--lc _NONE_(никакого параметра не надо указывать) Приведёт все пары к lowe_case. Это разумно сделать, потому что теперь необходиоые пары в тексте будут встречаться чаще  
2. Запустить python generate.py   
--model _Имя_Файла_ (Файл откуда будет подгружаться модель)   
--seed _Слово_ (Начальное слово. Если не укажите, то выберется любое слово на основе модели)  
--length _Int_ (Количество слов из котрых будет состоять текст)  
--output _Имя_Файла_ (Файл куда будет выгружаться текст. Если не укажите, то текст выведется в консоль)  
## Материалы
[Ссылка на тексты для обучения](https://drive.google.com/open?id=1hhU3HoljIiyO-2Bn0YtrFQqqi-Cw0MhF)

## Что нужно исправить
1 --help - работает коряво
