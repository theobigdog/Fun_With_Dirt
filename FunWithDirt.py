import pandas as pd
import numpy as np
import colorama
from colorama import Fore, Back, Style
import time
import random
import tabulate
from IPython.display import display
from xlwings import view
from pandas.core.base import PandasObject


p1_symbol = '☺'
p2_symbol = '☻'

fresh_board = pd.DataFrame(np.zeros((6, 7))).astype(int)
fresh_board = fresh_board.replace(0, '-')
fresh_board.index = [1,2,3,4,5,6]
fresh_board.columns = [1,2,3,4,5,6,7]

colors = ["Red", "Yellow", "Green", "Cyan", "Blue", "Magenta"]
colors_dict = {
    "Red" : Fore.RED + Style.BRIGHT,
    "Yellow" : Fore.YELLOW + Style.BRIGHT,
    "Green" : Fore.GREEN + Style.BRIGHT,
    "Cyan" : Fore.CYAN + Style.BRIGHT,
    "Blue" : Fore.BLUE + Style.BRIGHT,
    "Magenta" : Fore.MAGENTA + Style.BRIGHT,
}

def start_new_game(fresh_board):
    return fresh_board.copy()

def player_style(symbol, props=''):
    return props if symbol == p1_symbol else None

def display_board(current_board, players_dict):
    blank_index = [''] * len(current_board)
    current_board.index = blank_index
    print()
    p1_color = players_dict['p1']['color']
    p1_entry = f'{colors_dict[p1_color] + p1_symbol + Style.RESET_ALL}'
    p2_color = players_dict['p2']['color']
    p2_entry = f'{colors_dict[p2_color]}' + f'{p2_symbol + Style.RESET_ALL}'
    fixed = current_board.copy(deep=True).replace(p1_symbol, p1_entry)
    fixed = fixed.replace(p2_symbol, p2_entry)
    display(fixed)
    print()
    fixed2 = current_board.copy(deep=True).style.apply(player_style, props='color:magenta;')
    PandasObject.view = view
    current_board.view()
    #display(fixed2.to_markdown())


def get_choice(current_board):
    column = input('To which column will you be adding your coin?  ')
    try:
        column = int(column)
        if column in list(current_board.columns):
            return column
        else:
            column = get_choice(current_board)
            return column
    except(ValueError):
        column = get_choice(current_board)
        return column

def verify_enough_space(current_board, column):
    open_space = current_board[column] == '-'
    if any(open_space):
        return True
    else:
        print('There is no room in that column, please try again.')
        return False
    
def add_move(players_dict, whose_turn, current_board, column):
    board_index = np.arange(len(current_board), 1, -1).tolist()
    for pos in board_index:
        if current_board[pos-1][column-2] == '-':
            current_board.iat[pos-1,column-1] = players_dict[whose_turn]['symbol']
            break
    return current_board

def take_turn(whose_turn, current_board, players_dict):
    print(f"{players_dict[whose_turn]['name']}'s turn!")
    enough_space = False
    while not enough_space:
        column = get_choice(current_board)
        enough_space = verify_enough_space(current_board, column)
        if enough_space:
            current_board = add_move(players_dict, whose_turn, current_board, column)
            display_board(current_board, players_dict)
    return current_board

def welcome():
    print("Welcome to Connect Four!  An intense, cutting edge, nail-biter.  Play if you dare!")
    time.sleep(1)

def get_player_names():
    p1 = input('Player 1 Name?  ').title()
    p2 = input('Player 2 Name?  ').title()
    return [p1,p2]

def choose_color(player, available_colors):
    good = False
    while not good:
        print(f'{player}, please choose a color:')
        print()
        for color in available_colors:
            print(f'{colors_dict[color]}{color}' + Style.RESET_ALL)
        print()
        color = input()
        if type(color) == str and color.title() in available_colors:
            return color.title()
        print()
        print()

def get_player_colors(players, colors_dict = colors_dict):
    print()
    print()
    available_colors = colors
    p1_color = choose_color(players[0], available_colors)
    available_colors.remove(p1_color)
    p2_color = choose_color(players[1], available_colors)
    return [p1_color, p2_color]

def make_player_dict(players, player_colors):
    players_dict = {'p1' : {"name" : players[0], "color" : player_colors[0], "symbol" : p1_symbol}, 'p2' : {"name" : players[1], "color" : player_colors[1], "symbol" : p2_symbol}}
    return players_dict

def play_game(playing = True, current_board = start_new_game(fresh_board)):
    welcome()

    players = get_player_names()
    time.sleep(0.25)
    player_colors = get_player_colors(players)
    players_dict = make_player_dict(players, player_colors)

    display_board(current_board, players_dict)
    whose_turn = random.choice(list(players_dict.keys()))
    game_over = False

    while not game_over:
        current_board = take_turn(whose_turn, current_board, players_dict)
        if whose_turn == 'p1':
            whose_turn = 'p2'
        elif whose_turn =='p2':
            whose_turn = 'p1'
        #game_over = True

    while playing: # For adding in another game to follow
        playing = False
    #testing(current_board)

def testing(current_board):
    #print(current_board.iloc[0][7])
    #test_list = np.arange(len(current_board), 0, -1).tolist()
    #print(test_list)
    #tested = np.arange(17, 1, -1).tolist()
    #print(tested)
    for row in current_board[0]:
        print('firstfor')
        print(row)
        for col in range(len(current_board[row])):#current_board[row]:
            print('secondfor')
            print(col)
            print(current_board.at[row,col])

play_game()