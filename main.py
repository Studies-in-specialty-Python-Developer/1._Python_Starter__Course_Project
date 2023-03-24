import math
import os
import sys
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import colorama
from colorama import Fore, Style  # , Back
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import const


# Вместо кучи ифов можно использовать словари


def main():
    print_menu('Main menu', menu_txt['Main menu'], 3, 0, 7)
    menu_choice(main_menu_action)
    pass


def print_menu(header, items, header_indent, items_indent, rows):
    pt = PrettyTable(border=False, header=False, left_padding_width=items_indent)
    row_number = rows
    col_number = math.ceil(len(items) / row_number)
    while len(items) < row_number * col_number:
        items.append('')
    for col in range(col_number):
        pt.add_column(f'Column {col}', items[col * row_number:(col + 1) * row_number], align='l')
    os.system('cls')
    indent = ''.ljust(header_indent)
    print(Fore.BLUE + Style.DIM + f'{indent}{header}')
    print(pt)


def menu_choice(menu_action):
    correct_choice = False
    input_str = const.correct_input
    while not correct_choice:
        choice = input(input_str)
        if choice.isdigit() and int(choice) < len(menu_action):
            menu_action[choice](choice)
            correct_choice = True


def main_menu():
    pass
    # main_menu_txt = [f'{number}. {item}' for number, item in enumerate(const.main_menu_list, 1)]
    # correct_choice = False
    # input_str = const.correct_input
    # while not correct_choice:
    #     os.system('cls')
    #     print(Fore.BLUE + Style.DIM + '  Main menu')
    #     for item in main_menu_txt:
    #         print(item)
    #     print(Fore.RED + Style.DIM + '0. Exit')
    #     print()
    #     choice = input(input_str)
    #     if choice.isdigit() and int(choice) < 3:
    #         if choice == '0':  # 0. Exit
    #             sys.exit(0)
    #         if choice == '1':  # 1. Recommend the movie by genres
    #             submenu1()
    #         if choice == '2':  # 2. Recommend music by genres
    #             submenu2()
    #         if choice == '3':  # 3. Recommend the game by genres
    #             submenu3()
    #         # if choice == '4': # 4. Tell a joke
    #         #     submenu4()
    #         # if choice == '5': # 5. Tell an interesting story
    #         #     submenu5()
    #         # if choice == '6': # 6. Play the game
    #         #     submenu6()
    #         correct_choice = True
    #     else:
    #         input_str = const.incorrect_input
    #         correct_choice = False


def submenu1():
    submenu_1_txt = [f'{number:>2}. {item}' for number, item in
                     enumerate(const.submenu_1_list, 1)]
    submenu_1_txt.append(' 0. Return')
    submenu_1 = PrettyTable(border=False, header=False, left_padding_width=2)
    row_number = 5
    col_number = math.ceil(len(submenu_1_txt) / row_number)
    while len(submenu_1_txt) < row_number * col_number:
        submenu_1_txt.append('')
    for col in range(math.ceil(len(submenu_1_txt) / row_number)):
        submenu_1.add_column(f'Column {col}', submenu_1_txt[col * row_number:(col + 1) * row_number], align='l')
    os.system('cls')
    print(Fore.BLUE + Style.DIM + '  List of movie genres')
    print(submenu_1)
    print()
    correct_choice = False
    input_str = const.correct_input
    while not correct_choice:
        choice = input(input_str)
        if choice.isdigit() and int(choice) < len(submenu_1_txt):
            correct_choice = True
            if choice == '0':
                main_menu()
            else:
                submenu_1_proc(submenu_1_txt[int(choice) - 1])
        else:
            input_str = const.incorrect_input
            correct_choice = False


def submenu2():
    pass
    # submenu_2 = PrettyTable(border=False, header=False)
    # row_number = 15
    # col_number = math.ceil(len(submenu_2_txt) / row_number)
    # while len(submenu_2_txt) < row_number * col_number:
    #     submenu_2_txt.append('')
    # for col in range(math.ceil(len(submenu_2_txt) / row_number)):
    #     submenu_2.add_column(f'Column {col}', submenu_2_txt[col * row_number:(col + 1) * row_number], align='l')
    # os.system('cls')
    # print(Fore.BLUE + Style.DIM + '  List of music genres')
    # print(submenu_2)
    # print()
    # correct_choice = False
    # input_str = const.correct_input
    # while not correct_choice:
    #     choice = input(input_str)
    #     if choice.isdigit() and int(choice) < len(submenu_2_txt):
    #         correct_choice = True
    #         if choice == '0':
    #             main_menu()
    #         else:
    #             submenu_2_proc(submenu_2_txt[int(choice) - 1])
    #     else:
    #         input_str = const.incorrect_input
    #         correct_choice = False


def submenu3():
    response = requests.get('https://ag.ru/genres')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
    else:
        print('Ошибка при получении данных о жанрах игр: код', response.status_code)

    results = spotify.recommendation_genre_seeds()
    submenu_2_txt = [f'{number:>3}. {item}' for number, item in
                     enumerate(results.get('genres'), 1)]
    submenu_2_txt.append('  0. Return')
    submenu_2 = PrettyTable(border=False, header=False)
    row_number = 15
    col_number = math.ceil(len(submenu_2_txt) / row_number)
    while len(submenu_2_txt) < row_number * col_number:
        submenu_2_txt.append('')
    for col in range(math.ceil(len(submenu_2_txt) / row_number)):
        submenu_2.add_column(f'Column {col}', submenu_2_txt[col * row_number:(col + 1) * row_number], align='l')
    os.system('cls')
    print(Fore.BLUE + Style.DIM + '  List of music genres')
    print(submenu_2)
    print()
    correct_choice = False
    input_str = const.correct_input
    while not correct_choice:
        choice = input(input_str)
        if choice.isdigit() and int(choice) < len(submenu_2_txt):
            correct_choice = True
            if choice == '0':
                main_menu()
            else:
                submenu_2_proc(submenu_2_txt[int(choice) - 1])
        else:
            input_str = const.incorrect_input
            correct_choice = False


def submenu_1_proc(genre):
    pass


def submenu_2_proc(genre):
    pass


if __name__ == "__main__":
    # Инициализация модуля colorama
    colorama.init(autoreset=True)
    # Создание пунктов консольного меню в виде словаря
    main_menu_txt = ['Recommend the movie by genres', 'Recommend music by genres', 'Recommend the game by genres',
                     'Tell a joke', 'Tell an interesting story', 'Play the game']

    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(client_id=const.client_id,
                                                            client_secret=const.client_secret))
    music_genres_txt = spotify.recommendation_genre_seeds()

    menu_txt = {'Main menu': [f'{number}. {item}' for number, item in enumerate(main_menu_txt, 1)]}
    menu_txt['Main menu'].append('0. Exit')
    menu_txt['Music genres'] = [f'{number:>3}. {item}' for number, item in enumerate(music_genres_txt.get('genres'), 1)]
    menu_txt['Music genres'].append('  0. Return')

    main_menu_action = {
        '0': sys.exit,  # 0. Exit colorama.deinit ()
        '1': print,  # 1. Recommend the movie by genres
        '2': print,  # 2. Recommend music by genres
        '3': print,  # 3. Recommend the game by genres
        '4': print,  # 4. Tell a joke
        '5': print,  # 5. Tell an interesting story
        '6': print  # 6. Play the game
    }

    main()
