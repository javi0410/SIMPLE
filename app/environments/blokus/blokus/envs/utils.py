from src.constants import pieces, initial_board, match_enum, simple_pieces
from src.enums import Cell_type
import numpy as np
from ast import literal_eval

def all_moves(num_squares):
    moves = []
    for i in range(num_squares):
        for j in simple_pieces:
            moves.append([i] + j)
    return moves


def transform_to_3_values(board, player):
    new_board = np.array(board)
    if player == 2:
        new_board = np.rot90(new_board, 1)
    elif player == 3:
        new_board = np.rot90(new_board, 3)
    elif player == 4:
        new_board = np.rot90(new_board, 2)
    for i in range(1, 5):
        if i == player:
            new_board = np.where(new_board == player, 1, new_board)
        else:
            new_board = np.where(new_board == i, 2, new_board)
    return new_board


def transform_to_3_layers(new_board):
    matrix = []
    row = []
    for i in range(new_board.shape[0]):
        for j in new_board[i]:
            if j == 1:
                row.append(np.array([255, 0, 0]))
            elif j == 0:
                row.append(np.array([0, 255, 0]))
            else:
                row.append(np.array([0, 0, 255]))
        matrix.append(row)
        row = []
    return np.array(matrix)


def mark_enviroment_from_cell(board, player, i, j):
    hot_cell_value = match_enum[player]
    try:
        # check top_empty side
        if board[i - 1][j] != player:
            board[i - 1][j] = Cell_type.TEMP_UNAVAILABLE.value
            top_empty = True
        else:
            top_empty = False
    except:
        top_empty = False

    try:
        # check top side
        if board[i][j - 1] != player:
            board[i][j - 1] = Cell_type.TEMP_UNAVAILABLE.value
            left_empty = True
        else:
            left_empty = False
    except:
        left_empty = False

    try:
        # check right side
        if board[i][j + 1] != player:
            board[i][j + 1] = Cell_type.TEMP_UNAVAILABLE.value
            right_empty = True
        else:
            right_empty = False
    except:
        right_empty = False

    try:
        # check bottom side
        if board[i + 1][j] != player:
            board[i + 1][j] = Cell_type.TEMP_UNAVAILABLE.value
            bottom_empty = True
        else:
            bottom_empty = False
    except:
        bottom_empty = False

    hot_cell_values = []
    if bottom_empty and left_empty and board[i + 1][j - 1] == Cell_type.EMPTY.value and board[i + 2][
        j - 1] != player and board[i + 1][j - 2] != player:
        board[i + 1][j - 1] = hot_cell_value
        hot_cell_values.append((j - 1, i + 1))
    if bottom_empty and right_empty and board[i + 1][j + 1] == Cell_type.EMPTY.value and board[i + 2][
        j + 1] != player and board[i + 1][j + 2] != player:
        board[i + 1][j + 1] = hot_cell_value
        hot_cell_values.append((j + 1, i + 1))
    if top_empty and left_empty and board[i - 1][j - 1] == Cell_type.EMPTY.value and board[i - 2][j - 1] != player and \
            board[i - 1][j - 2] != player:
        board[i - 1][j - 1] = hot_cell_value
        hot_cell_values.append((j - 1, i - 1))
    if top_empty and right_empty and board[i - 1][j + 1] == Cell_type.EMPTY.value and board[i - 2][j + 1] != player and \
            board[i - 1][j + 2] != player:
        board[i - 1][j + 1] = hot_cell_value
        hot_cell_values.append((j + 1, i - 1))
    return hot_cell_values
