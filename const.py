input_str = {
    'correct': '    Enter your choice: ',
    'incorrect': '    You choice is incorrect. Please try again: '
}

menu_param = [{'header': 'Main menu',
               'number': 0, 'header_indent': 3, 'num_rjust': 0, 'column_padding': 0, 'row_count': 5},
              {'header': 'List of movie genres',
               'number': 1, 'header_indent': 4, 'num_rjust': 2, 'column_padding': 0, 'row_count': 5},
              {'header': 'List of music genres',
               'number': 2, 'header_indent': 5, 'num_rjust': 3, 'column_padding': 0, 'row_count': 15},
              {'header': 'List of joke category',
               'number': 3, 'header_indent': 3, 'num_rjust': 0, 'column_padding': 0, 'row_count': 4},
              {'header': 'Play the game',
               'number': 4, 'header_indent': 3, 'num_rjust': 0, 'column_padding': 0, 'row_count': 5},
              ]

main_menu_items = ['Recommend the movie by genres', 'Recommend music by genres', 'Tell a joke', 'Play the game']

movie_genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary',
                'Drama', 'Family', 'Fantasy', 'Film Noir', 'History', 'Horror', 'Music', 'Musical',
                'Mystery', 'Romance', 'Sci - Fi', 'Short Film', 'Sport', 'Superhero', 'Thriller',
                'War', 'Western']

jokes_genres = {'menu': ['Neutral geek jokes', 'Chuck Norris geek jokes', 'All jokes'],
                'param': ['neutral', 'chuck', 'all']}
