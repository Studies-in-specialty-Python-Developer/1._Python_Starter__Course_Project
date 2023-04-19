""" Модуль содержит константы и настройки, необходимые для работы основного модуля main.py"""

# Шаблоны строк ввода выбора пользователя
INPUT_STR = {
    'correct': '    Enter your choice: ',
    'incorrect': '    You choice is incorrect. Please try again: ',
    'correct_gallows': 'Enter your letter (0 - Return): ',
    'incorrect_gallows': 'You input is incorrect. Please try again (0 - Return): ',
}

# Параметры меню: заголовок, номер, отступ цифр номеров пунктов, расстояние между колонками, кол-во строк в колонке
MENU_PARAM = [{'header': 'Main menu',
               'number': 0, 'header_indent': 3, 'num_rjust': 0, 'column_padding': 0, 'row_count': 5},
              {'header': 'List of movie genres',
               'number': 1, 'header_indent': 4, 'num_rjust': 2, 'column_padding': 0, 'row_count': 5},
              {'header': 'List of music genres',
               'number': 2, 'header_indent': 5, 'num_rjust': 3, 'column_padding': 0, 'row_count': 15},
              {'header': 'List of joke category',
               'number': 3, 'header_indent': 3, 'num_rjust': 0, 'column_padding': 0, 'row_count': 4},
              {'header': 'Play the game',
               'number': 4, 'header_indent': 3, 'num_rjust': 0, 'column_padding': 0, 'row_count': 2},
              ]

# Пункты главного меню
MAIN_MENU_ITEMS = ['Recommend the movie by genres', 'Recommend music by genres', 'Tell a joke', 'Play the game']

# Жанры фильмов
MOVIE_GENRES = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
                'Drama', 'Family', 'Fantasy', 'Film Noir', 'History', 'Horror', 'Music', 'Musical',
                'Mystery', 'Romance', 'Sci - Fi', 'Short Film', 'Sport', 'Superhero', 'Thriller',
                'War', 'Western']

# Темы шуток
JOKES_GENRES = {'menu': ['Neutral geek jokes', 'Chuck Norris geek jokes', 'All jokes'],
                'param': ['neutral', 'chuck', 'all']}

# Шаблон виселицы
GALLOWS_PATTERN = [list(' +-----+'),
                   list(' |    \\|'),
                   list('       |'),
                   list('       |'),
                   list('       |'),
                   list('      /|\\'),
                   list('==========')]
