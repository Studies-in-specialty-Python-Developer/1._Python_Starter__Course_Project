import json
import math
import os
import sys
from pprint import pprint
from prettytable import PrettyTable
import colorama
from colorama import Fore, Style  # , Back
import spotipy
from pyjokes import pyjokes
from spotipy.oauth2 import SpotifyClientCredentials
import const
import conf_const


def main():
    main_menu(0)


def print_menu(menu_numb):
    header: str = ''
    items: list = []
    row_count = const.menu_param.get(menu_numb)['row_count']
    for header, items in menu_txt.get(menu_numb).items():
        pass
    column_count = math.ceil(len(items) / row_count)
    while len(items) < row_count * column_count:
        items.append('')
    pt = PrettyTable(border=False, header=False, left_padding_width=const.menu_param.get(menu_numb)['column_padding'])
    for col in range(column_count):
        pt.add_column(f'Column {col}', items[col * row_count:(col + 1) * row_count], align='l')
    os.system('cls')
    print(Fore.BLUE + Style.DIM + f'{" " * const.menu_param[menu_numb]["header_indent"]}{header}')
    print(pt)


def menu_choice(menu_numb):
    correct_choice = False
    input_str = const.correct_input
    while not correct_choice:
        if input_str == const.correct_input:
            print(input_str, end=' ')
        else:
            print(Fore.RED + Style.DIM + input_str, end=' ')
        choice = input()
        if choice.isdigit() and int(choice) < len(menu_action.get(menu_numb)):
            menu_action.get(menu_numb)[int(choice)](int(choice))
            input_str = const.correct_input
        else:
            correct_choice = False
            input_str = const.incorrect_input


def main_menu(menu_numb):
    print_menu(menu_numb)
    menu_choice(menu_numb)


def submenu(menu_numb):
    print_menu(menu_numb)
    menu_choice(menu_numb)


def menu_add(menu_numb: int, items: list) -> dict:
    # Нумеруем пункты меню
    numbering_items = [str(number).rjust(const.menu_param[menu_numb]["num_rjust"]) + '. ' + item
                       for number, item in enumerate(items)]
    # Делаем циклическую перестановку пунктов меню вправо на один шаг и добавляем заголовок
    return {const.menu_param[menu_numb]["header"]: numbering_items[1:] + numbering_items[:1]}


def de_numerate(menu_item: str) -> str:
    return menu_item[menu_item.find('. ') + 2:]


def get_movie(genre: int):
    print(genre)


def get_music(genre: int):
    genre_txt = de_numerate(list(menu_txt.get(2).values())[0][genre - 1])
    results = spotify.search(q='genre:' + genre_txt, type='artist').get('artists').get('items')
    # for item in results:
    pprint(results)


def get_joke(genre: int):
    print(pyjokes.get_joke(category=const.pyjokes_genre.get(genre)))


def get_play(genre: int):
    print(genre)


if __name__ == "__main__":
    # Инициализация модуля colorama
    colorama.init(autoreset=True)

    # Формирование текстов консольного меню в виде списка словарей,
    # у каждого меню свой номер, список пунктов и параметры
    # Формирование списка действий консольного меню в виде списка словарей, у каждого списка свой номер

    menu_txt = {}
    menu_action = {}

    menu_number = 0  # Main menu

    menu_items = ['Exit', 'Recommend the movie by genres', 'Recommend music by genres',
                  'Tell a joke', 'Play the game']
    menu_txt[menu_number] = menu_add(menu_number, menu_items)
    menu_action[menu_number] = {
        0: sys.exit,  # 0. Exit
        1: submenu,  # 1. Recommend the movie by genres
        2: submenu,  # 2. Recommend music by genres
        3: submenu,  # 3. Tell a joke
        4: submenu,  # 4. Play the game
    }

    menu_number = 1  # 1. Recommend the movie by genres

    menu_items = ['Return']
    menu_txt[menu_number] = menu_add(menu_number, menu_items)
    menu_action[menu_number] = {i: main_menu if i == 0 else get_movie for i in range(1)}  # 0. Main menu 1-1. get_movie

    menu_number = 2  # 2. Recommend music by genres

    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(client_id=conf_const.spotify['client_id'],
                                                            client_secret=conf_const.spotify['client_secret']))
    menu_items = spotify.recommendation_genre_seeds().get('genres')
    menu_items.insert(0, 'Return')
    menu_txt[menu_number] = menu_add(menu_number, menu_items)
    menu_action[menu_number] = {i: main_menu if i == 0 else get_music for i in range(len(menu_items))}
    # 0. Main menu 1-125. get_music

    menu_number = 3  # 3. Tell a joke

    menu_items = ['Return', 'Neutral geek jokes', 'Chuck Norris geek jokes', 'All jokes']
    menu_txt[menu_number] = menu_add(menu_number, menu_items)
    menu_action[menu_number] = {i: main_menu if i == 0 else get_joke for i in range(len(menu_items))}
    # 0. Main menu 1-3. get_joke

    menu_number = 4  # 4. Play the game

    menu_items = ['Return']
    menu_txt[menu_number] = menu_add(menu_number, menu_items)
    menu_action[menu_number] = {i: main_menu if i == 0 else get_play for i in range(1)}  # 0. Main menu 1-1. get_play
    pprint(menu_txt)
    pprint(menu_action)
    main()
