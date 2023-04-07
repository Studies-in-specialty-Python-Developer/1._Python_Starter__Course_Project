""" Модуль реализует функционал развлекательного чат-бота. Данный бот может рекомендовать фильмы
и музыку по жанрам, рассказывать шутки, а также дать возможность поиграть в игру """

import copy
import math
import os
import sys
from pprint import pprint
import imdb
from faker import Faker
from prettytable import PrettyTable
import colorama
from colorama import Fore, Style  # , Back
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyjokes import pyjokes
import const
import conf_const


def main():
    """ Основная функция, в которой инициализируется модуль colorama и вызывается главное меню """

    # Инициализация модуля colorama
    colorama.init(autoreset=True)

    main_menu(0)


def print_menu(menu_number: int):
    """ Выводит в консоль меню с заданным номером
        Arguments:
        menu_number: int - номер меню"""
    param = get_menu_param(menu_number)
    items = list(all_menu.get(param['header'], {}).keys())
    column_count = math.ceil(len(items) / param.get('row_count', 1))
    while len(items) < param.get('row_count', 1) * column_count:
        items.append('')
    pretty_table = PrettyTable(border=False, header=False, left_padding_width=param['column_padding'])
    for col in range(column_count):
        pretty_table.add_column(f'Column {col}',
                                items[col * param.get('row_count', 1):(col + 1) * param.get('row_count', 1)],
                                align='l')
    os.system('cls')
    print(Fore.BLUE + Style.DIM + f'{" " * param["header_indent"]}{param["header"]}')
    print(pretty_table)


def menu_choice(menu_number: int):
    """ Реализует выбор пользователем пункта меню в консоли для меню с заданным номером
        Arguments:
        menu_number: int - номер меню"""
    actions = list(all_menu.get(get_menu_param(menu_number).get('header'), {}).values())
    correct_choice = False
    input_str = const.input_str.get('correct', '')
    while not correct_choice:
        if input_str == const.input_str.get('correct'):
            print(input_str, end=' ')
        else:
            print(Fore.RED + Style.DIM + input_str, end=' ')
        choice = input()
        if choice.isdigit() and int(choice) < len(actions):
            action_position = len(actions) - 1 if choice == '0' else int(choice) - 1
            actions[action_position](int(choice))
            input_str = const.input_str.get('correct', '')
        else:
            correct_choice = False
            input_str = const.input_str.get('incorrect', '')


def main_menu(menu_number: int):
    """ Выводит в консоль главное меню, которое имеет номер 0
        Arguments:
        menu_number: int - номер меню"""
    print_menu(menu_number)
    menu_choice(menu_number)


def submenu(menu_number: int):
    """ Выводит в консоль подменю, которое имеет номер menu_number
        Arguments:
        menu_number: int - номер меню"""
    # Возможно, имеет смысл объединить в одну функции main_menu и submenu, но тогда возможны странные рекурсии
    print_menu(menu_number)
    menu_choice(menu_number)


def get_movie(genre: int):
    """ Выводит в консоль список рекомендуемых фильмов заданного жанра
        Arguments:
        genre: int - кодовый номер жанра фильма"""
    get_movie_menu_txt = list(all_menu.get(get_menu_param(1).get('header'), {}).keys())
    genre_txt = de_numerate_menu_item(get_movie_menu_txt[genre - 1])
    response = imdb.IMDb().get_top50_movies_by_genres(genre_txt)
    result = []
    for item in response:
        movie_id = item.movieID
        resume = {'Title': str(item)}
        resume.update({'URL': f'https://www.imdb.com/title/tt{movie_id}/'})
        result.append(resume)
        pprint(resume, sort_dicts=False)
        print()


def get_music(genre: int):
    """ Выводит в консоль список рекомендуемой музыки заданного жанра
        Arguments:
        genre: int - кодовый номер жанра музыки"""
    get_music_menu_txt = list(all_menu.get(get_menu_param(2).get('header'), {}).keys())
    genre_txt = de_numerate_menu_item(get_music_menu_txt[genre - 1])
    response = spotify.search(q='genre:' + genre_txt, type='artist').get('artists').get('items')
    result = []
    for item in response:
        resume = {'Name': item.get('name')}
        resume.update({'Genres': ', '.join(item.get('genres'))})
        resume.update({'Popularity': item.get('popularity')})
        resume.update({'Followers': item.get('followers').get('total')})
        resume.update({'URL': item.get('external_urls').get('spotify')})
        result.append(resume)
        pprint(resume, sort_dicts=False)
        print()


def get_joke(genre: int):
    """ Выводит в консоль шутку на одну из заданных тем
        Arguments:
        genre: int - кодовый номер темы шутки"""
    print(pyjokes.get_joke(category=const.jokes_genres.get('param', '')[genre - 1]))
    print()


def get_play(genre: int):
    """ Выводит в консоль игру "Виселица", в которой надо угадать название страны
        Arguments:
        genre: int - кодовый номер игры"""
    if genre == 1:
        def print_gallows():
            os.system('cls')
            print(first_str)
            if errors > 0:
                gallows[2][1] = 'O'  # голова
            if errors > 1:
                gallows[3][1] = '|'  # туловище
            if errors > 2:
                gallows[3][0] = '/'  # левая рука
            if errors > 3:
                gallows[3][2] = '\\'  # правая рука
            if errors > 4:
                gallows[4][0] = '/'  # левая нога
            if errors > 5:
                gallows[4][2] = '\\'  # правая нога
            for _ in gallows:
                print(''.join(_))
            print(' '.join(mask_str))
            if wrong_letters:
                print(Fore.RED + Style.DIM + 'Wrong: ' + ' '.join(wrong_letters))

        gallows = copy.deepcopy(const.gallows_pattern)
        fake = Faker()
        country_name = str(fake.country())
        while ' ' in country_name:
            country_name = str(fake.country())
        first_str = 'Guess the country name!'
        mask_str = list('_' * len(country_name))
        wrong_letters = []
        errors = 0
        game_on = True
        choice: str = ''
        while game_on:
            print_gallows()
            correct_choice = False
            input_str = const.input_str.get('correct_gallows', '')
            while not correct_choice:
                if input_str == const.input_str.get('correct_gallows'):
                    print(input_str, end=' ')
                else:
                    print(Fore.RED + Style.DIM + input_str, end=' ')
                choice = input()
                if all([len(choice) == 1, any([choice.isalpha(), choice == '0'])]):
                    correct_choice = True
                    input_str = const.input_str.get('correct_gallows', '')
                else:
                    correct_choice = False
                    input_str = const.input_str.get('incorrect_gallows', '')
            if choice.lower() in country_name.lower():
                for number, item in enumerate(country_name.lower()):
                    if item == choice.lower():
                        mask_str[number] = item
                mask_str[0] = mask_str[0].capitalize()
            else:
                wrong_letters.append(choice.lower())
                errors += 1
            if errors == 6:
                game_on = False
                print(Fore.RED + Style.DIM + 'G a m e  O v e r !')
                print('This country -', country_name)
                choice = input()
                submenu(4)
            if '_' not in ''.join(mask_str):
                game_on = False
                print(Fore.GREEN + Style.DIM + 'Y o u  W i n !')
                choice = input()
                submenu(4)
            if choice == '0':
                submenu(4)


def add_menu_items(menu_number: int, items_txt: list, handler, last_item_key: str, last_item_handler) -> dict:
    """ Формирует одно из меню
        Arguments:
        menu_number: int - номер меню, соответсвующий номеру из константы "menu_param" модуля "const.py"
        items_txt: list - список, содержащий тексты пунктов меню
        handler - ссылка на функцию, обрабатывающую выбор пунктов меню, кроме последнего
        last_item_key: str - текст последнего пункта меню, обычно "Return"
        last_item_handler - ссылка на функцию, обрабатывающую выбор последнего пункта меню
        Returns:
        dict - словарь, содержащий тексты пунктов меню и соответствующие им обработчики (ссылки на функции)
        * пример структуры меню в файле notes.txt"""
    num_rjust = get_menu_param(menu_number).get('num_rjust', 0)
    # Нумеруем пункты меню
    menu_txt = [str(number).rjust(num_rjust) + '. ' + item for number, item in enumerate(items_txt, 1)]
    # Составляем список с действиями к каждому пункту меню
    actions = [handler for _ in range(len(menu_txt))]
    # Создаем словарь с пунктами меню и соответствующими действиями
    menu_items = dict(zip(menu_txt, actions))
    # Добавляем последним пункт меню для возврата в главное меню или выхода из программы
    menu_items[' ' * (num_rjust - 1) + last_item_key] = last_item_handler
    return menu_items


def de_numerate_menu_item(menu_item: str) -> str:
    """ Убирает номер в тексте заданного пункта меню
        Arguments:
        menu_item: str - текст пункта меню с номером
        Returns:
        str - текст пункта меню без номера"""
    return menu_item[menu_item.find('. ') + 2:]


def get_menu_param(menu_number: int) -> dict:
    """ Возвращает словарь, содержащий свойства заданного меню из константы "menu_param" модуля "const.py"
        Arguments:
        menu_number: int - номер меню, соответсвующий номеру из константы "menu_param" модуля "const.py"
        Returns:
        dict - словарь, содержащий свойства заданного меню из константы "menu_param" модуля "const.py"
        """
    result = {}
    for item in const.menu_param:
        if item['number'] == menu_number:
            result = item
    return result


if __name__ == "__main__":
    # Получение списка жанров музыки с сайта Spotify.com
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(client_id=conf_const.spotify['client_id'],
                                                            client_secret=conf_const.spotify['client_secret']))
    music_genres = spotify.recommendation_genre_seeds().get('genres')

    # Формирование текстов и действий пунктов консольного меню в виде списка словарей,
    # у каждого меню свой номер, название, параметры, список пунктов и список действий
    # Пример структуры меню есть в файле notes.txt

    all_menu = {get_menu_param(0).get('header'): add_menu_items(0,  # 'Main menu'
                                                                const.main_menu_items, submenu, '0. Exit', sys.exit),
                get_menu_param(1).get('header'): add_menu_items(1,  # 'List of movie genres'
                                                                const.movie_genres, get_movie, '0. Return', main_menu),
                get_menu_param(2).get('header'): add_menu_items(2,  # 'List of music genres'
                                                                music_genres, get_music, '0. Return', main_menu),
                get_menu_param(3).get('header'): add_menu_items(3,  # 'List of joke category'
                                                                const.jokes_genres.get('menu', []), get_joke,
                                                                '0. Return', main_menu),
                get_menu_param(4).get('header'): add_menu_items(4,  # 'Play the game'
                                                                ['Guess the country name'], get_play, '0. Return',
                                                                main_menu)
                }

    main()
