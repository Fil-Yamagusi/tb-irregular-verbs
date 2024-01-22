#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""2024-01-12 Fil - Future code Yandex.Practicum
Бот-квест "Экзамен по неправильным английским глаголам"
Описание в README.md

Разные словари и списки. Вынес, чтобы место не занимали
"""

# Три класса персонажа.
rpg_classes = {
    'geek': 'Гик',
    'nerd': 'Отличница',
    'idler': 'Лентяй',
}

# У каждого свой предмет волшебный.
rpg_items = {
    'geek': {
        'name': 'Вибробраслет',
        'description':
            'Схему вибробраслета на arduino предложил блогер AlexGyver: '
            'надевается на большой палец ноги. Управляется '
            'движением пальца, ответ - тихой вибрацией.',
        'fail':
            'Вышло всё, как в фильме про Шурика: <i>профессор - лопух, но '
            'аппаратура при нём, при нём</i>. Вибробраслет начал свистеть, '
            'жужжать, хрипеть. Подошёл Проверяющий с улыбкой и показал '
            'глушилку всех гаджетов. Тебя с позором вывели из аудитории.',
        'success':
            'AlexGyver отличную электронную шпаргалку изобрёл! Проверяющий '
            'видит, как ты барабанишь пальцами по парте, а потом резко '
            'вписываешь ответ. И так до конца листа! С видом победителя '
            'ты сдаёшь работу.',
    },
    'nerd': {
        'name': 'Структурированная вода',
        'description':
            'Бутылочка структурированный воды с памятью. Несколько раз '
            'прочитать рядом с бутылочкой вслух таблицу глаголов. Когда '
            'будешь пить - вода передаст тебе сохранённую информацию.',
        'fail':
            'Информация в воде переструктурировалась во время тренировки '
            'с Катей. Вода "слышала" неправильные ответы, вся запуталась '
            'и вообще! Найти бы того, кто посоветовал эту глупость, и '
            'заставить читать чайнику всю Большую советскую энциклопедию!',
        'success':
            'Вот это да! Память воды сработала! Или торсионные поля '
            'ретроградного Меркурия удачно оттопырили твои чакры. Так или '
            'иначе - ты с гордым видом сдаёшь лист со всеми ответами!',
    },
    'idler': {
        'name': 'Микрошпаргалка',
        'description':
            'Шпаргалка с мелким-мелким шрифтом, распечатанная на принтере. '
            'Выглядит как лист из тетради в линейку.',
        'fail':
            'Ловкости тебе не занимать, а вот лень снова подвела. Надо было '
            'проверить таблицу, а не распечатывать первую ссылку поисковика '
            'по запросу <i>шпаргалка неправильных глаголов</i>. '
            'У тебя на распечатке текст не в той кодировке!\n\n'
            'чПМЗБ ЧРБДБЕФ Ч ЛБУРЙКУЛПЕ НПТЕ иНЖАЛИД ДЕЖИЦЕ. бНОПНЯ: йЮЙ '
            'ОЕПЕЙКЧВЮРЭ ЙНДХПНБЙС?',
        'success':
            'Высокие технологии и хорошее зрение очень пригодились! На '
            'каждый вопрос нашёлся подходящий ответ. И ни один из '
            'Проверяющих не заметил нарушения.',
    },
    'common': {
        'name': 'None',
        'description': 'None',
        'fail': 'None',
        'success':
            'Молодец! За границей потом будешь говорить иностранцам: '
            '<i>thinked, buyed, flyed, drinked...</i> '
            'Ну а чо? Им надо, пусть они и понимают!',
    },
}

# имя отчество преподавателя для ловушки
teacher_names = [
    "Глафира Бэкингемовна",
    "Злата Виндзоровна",
    "Жозефина Генриеттовна",
    "Генриетта Жозефиновна",
    "Клавдия Сильвестровна",
    "Дьюти Тудеевна",
    "Анна Сэндвичевна",
    "Варвара Биг-Беновна",
    "Дарья Беконовна",
    "Елена Парламентoвнa",
    "Зинаида Бутербродовна",
    "Кристина Лондоновна",
    "Лариса Ливерпулевна",
    "Мария Тауэрсовна",
    "Наталья Бристолевна",
    "Ольга Борнмутовна",
    "Полина Хот-Договна",
    "София Чарльзовна",
    "Виктория Альбертовна",
    "Виктория Бэкхемовна",
    "Диана Чарльзовна",
    "Юлия Стоунхенжевна",
    "Мэри Борнмутовна",
    "Элизабет Стюартовна",
    "Елизавета Яковлевна",
    "Мэри Ричардовна",
    "Мэри Генриховна",
    "Джейн Греевна",
    "Елизавета Эдуардовна",
    "Джульетта Шекспировна",
    "Дездемона Отелловна",
    "Пиппа Филипповна",
    "Виктория Вильгельмовна",
    "Елизавета Георгевна",
]

# Похвала на английском для локации КАБИНЕТ ХИМИИ (3 из 4)
right_answer = [
    "Excellent", "Right answer", "Correct!", "Right!", "True!",
    "Exactly", "Good for you", "Well done", "Good job", "Great",
    "Brilliantly", "Nicely done", "Molodets!", "Umnitsa!",
]

# шмишьные фразочки для локации КАБИНЕТ АНГЛИЙСКОГО (3 из 4)
spooky = [
    "Ты рассеянно думаешь: 'странно, ведь <i>Two</i>, а не <i>Два</i>?'",
    "От жути зубы ходят ходуном.",
    "Страх леденит от мозга костей до костей мозга.",
    "Страшно до кожаных мурашек.",
    "От ужаса волосы стынут в жилах.",
    "От страха кровь становится дыбом.",
    "Почему-то так домой захотелось, котика обнять...",
]

# имена друзей для локации КАБИНЕТ АНГЛИЙСКОГО (3 из 4)
friends = [
    "Петя", "Вася", "Саша", "Коля", "Толя", "Андрей",
    "Лёха", "Серёга", "Костян", "Вадим", "Артём", "Вова",
]

# шмишьные подписи под карикатурой в локации ЭКЗАМЕН (4 из 4)
caricature = [
    "Хэрок эскусто бэн шлак мордюк!",
    "Хэрок эскусс мордюк, тобиш нак!",
    "Мы вас любим… в глубине души. Где-то очень глубоко.",
    "Ну почему же крашена? Это мой натуральный цвет!",
    "Бабу Ягу со стороны брать не будем – воспитаем в своем коллективе.",
    "Паки, паки... иже херувимы!",
    "Наши люди в булочную на такси не ездят.",
    "Если человек идиот, то это надолго.",
    "Бамбарбия. Кергуду.",
    "Руссо туристо. Облико морале!",
    "Тебя посодют, а ты не воруй!",
    "Не люблю я таких людей! Непунктуальных!",
    "Шампанское по утрам пьют или аристократы, или дегенераты.",
]

# эпитеты для откинувшегося друга (3 из 4)
why = [
    "Откуда у него седина?!", "Почему у него дёргается глаз?",
    "Стоит ни жив, ни мёртв.", "Он как будто постарел!",
    "Он бледнее смерти.", "Бледный, как мел!",
]

# эпитеты для смеха в ответ на шутку преподавателя (4 из 4)
how = [
    "угодливо", "заискивающе", "подхалимски",
    "подобострастно", "неискренне", "робко",
]
