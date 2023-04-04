import math
import os
import sys
import imdb
from pprint import pprint
from prettytable import PrettyTable
import colorama
from colorama import Fore, Style  # , Back
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyjokes import pyjokes
import const
import conf_const


def main():
    main_menu(0)


def print_menu(menu_number: int):
    param = get_menu_param(menu_number)
    items = list(all_menu.get(param['header']).keys())
    column_count = math.ceil(len(items) / param.get('row_count'))
    while len(items) < param.get('row_count') * column_count:
        items.append('')
    pt = PrettyTable(border=False, header=False, left_padding_width=param['column_padding'])
    for col in range(column_count):
        pt.add_column(f'Column {col}', items[col * param.get('row_count'):(col + 1) * param.get('row_count')],
                      align='l')
    os.system('cls')
    print(Fore.BLUE + Style.DIM + f'{" " * param["header_indent"]}{param["header"]}')
    print(pt)


def menu_choice(menu_number: int):
    actions = list(all_menu.get(get_menu_param(menu_number).get('header')).values())
    correct_choice = False
    input_str = const.input_str.get('correct')
    while not correct_choice:
        if input_str == const.input_str.get('correct'):
            print(input_str, end=' ')
        else:
            print(Fore.RED + Style.DIM + input_str, end=' ')
        choice = input()
        if choice.isdigit() and int(choice) < len(actions):
            action_position = len(actions) - 1 if choice == '0' else int(choice) - 1
            actions[action_position](int(choice))
            input_str = const.input_str.get('correct')
        else:
            correct_choice = False
            input_str = const.input_str.get('incorrect')


def main_menu(menu_number: int):
    print_menu(menu_number)
    menu_choice(menu_number)


def submenu(menu_number: int):
    print_menu(menu_number)
    menu_choice(menu_number)


def get_movie(genre: int):
    get_movie_menu_txt = list(all_menu.get(get_menu_param(1).get('header')).keys())
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
    get_music_menu_txt = list(all_menu.get(get_menu_param(2).get('header')).keys())
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
    print(pyjokes.get_joke(category=const.jokes_genres.get('param')[genre - 1]))
    print()


def get_play(genre: int):
    print(genre - 1)


def add_menu_items(menu_number: int, items_txt: list, handler, last_item_key: str, last_item_handler) -> dict:
    num_rjust = get_menu_param(menu_number).get('num_rjust')
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
    return menu_item[menu_item.find('. ') + 2:]


def get_menu_param(menu_number: int) -> dict:
    for item in const.menu_param:
        if item['number'] == menu_number:
            return item


if __name__ == "__main__":
    # Инициализация модуля colorama
    colorama.init(autoreset=True)

    # Получение списка жанров музыки с сайта Spotify.com
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(client_id=conf_const.spotify['client_id'],
                                                            client_secret=conf_const.spotify['client_secret']))
    music_genres = spotify.recommendation_genre_seeds().get('genres')

    # Формирование текстов и действий пунктов консольного меню в виде списка словарей,
    # у каждого меню свой номер, название, параметры, список пунктов и список действий

    all_menu = {get_menu_param(0).get('header'): add_menu_items(0,  # 'Main menu'
                                                                const.main_menu_items, submenu, '0. Exit', sys.exit),
                get_menu_param(1).get('header'): add_menu_items(1,  # 'List of movie genres'
                                                                const.movie_genres, get_movie, '0. Return', main_menu),
                get_menu_param(2).get('header'): add_menu_items(2,  # 'List of music genres'
                                                                music_genres, get_music, '0. Return', main_menu),
                get_menu_param(3).get('header'): add_menu_items(3,  # 'List of joke category'
                                                                const.jokes_genres.get('menu'), get_joke,
                                                                '0. Return', main_menu),
                get_menu_param(4).get('header'): add_menu_items(4,  # 'Play the game'
                                                                ['Game'], get_play, '0. Return', main_menu)
                }

    pprint(all_menu, sort_dicts=False)

    main()
