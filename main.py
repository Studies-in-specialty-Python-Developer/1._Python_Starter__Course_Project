import os
from prettytable import PrettyTable

import const


def main():
    mainmenu()


def mainmenu():
    main_menu_txt = [f'{number}. {item}' for number, item in enumerate(const.main_menu_list, 1)]
    main_menu_txt.append('0. Exit\n')
    main_menu_txt.insert(0, '  Main menu')
    main_menu = '\n'.join(main_menu_txt)
    correct_choice = False
    input_str = const.correct_input
    while not correct_choice:
        os.system('cls')
        print(main_menu)
        choice = input(input_str)
        if choice.isdigit() and int(choice) < 2:
            if choice == '1':
                submenu1()
            # if choice == '2':
            #     submenu2()
            # if choice == '3':
            #     submenu3()
            # if choice == '4':
            #     submenu4()
            # if choice == '5':
            #     submenu5()
            # if choice == '6':
            #     submenu6()
            # if choice == '7':
            #     submenu7()
            correct_choice = True
        else:
            input_str = const.incorrect_input
            correct_choice = False


def submenu1():
    submenu_1_txt = [f'{number}. {item}' for number, item in
                     enumerate(const.submenu_1_list, 1)]
    submenu_1_txt.append(' 0. Return\n')
    submenu_1 = PrettyTable()
    for col in range(int(len(submenu_1_txt) / 5)):
        submenu_1.add_column(f'Column {col}', submenu_1_txt[col * 5:(col + 1) * 5], align='l')
    os.system('cls')
    print('  List of movie genres')
    print(submenu_1)
    correct_choice = False
    input_str = const.correct_input
    while not correct_choice:
        choice = input(input_str)
        if choice.isdigit() and int(choice) < len(submenu_1_txt):
            submenu_1_1(submenu_1_txt[int(choice) - 1])
            correct_choice = True
        else:
            input_str = const.incorrect_input
            correct_choice = False


def submenu_1_1(genre):
    pass


if __name__ == "__main__":
    main()
