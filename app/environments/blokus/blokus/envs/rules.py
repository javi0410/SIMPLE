import numpy as np
from termcolor import colored
import copy
import sys


def has_adyacent_occupied_cells(reshaped_board, x, y, player_symbol):
    try:
        if reshaped_board[x + 1][y].symbol == player_symbol:
            return True
    except:
        pass
    try:
        if (x - 1) >= 0 and \
                reshaped_board[x - 1][y].symbol == player_symbol:
            return True
    except:
        pass
    try:
        if (y - 1) >= 0 and \
                reshaped_board[x][y - 1].symbol == player_symbol:
            return True
    except:
        pass
    try:
        if reshaped_board[x][y + 1].symbol == player_symbol:
            return True
    except:
        pass

    return False


def is_hot_cell(reshaped_board, x, y, player_symbol):
    if reshaped_board[x][y].symbol != ".":
        return False
    if has_adyacent_occupied_cells(reshaped_board, x, y, player_symbol):
        return False
    try:
        if reshaped_board[x + 1][y + 1].symbol == player_symbol:
            return True
    except:
        pass
    try:
        if (x - 1) >= 0 and \
                reshaped_board[x - 1][y + 1].symbol == player_symbol:
            return True
    except:
        pass
    try:
        if (y - 1) >= 0 and \
                reshaped_board[x + 1][y - 1].symbol == player_symbol:
            return True
    except:
        pass
    try:
        if (y - 1) >= 0 and (x - 1) >= 0 and \
                reshaped_board[x - 1][y - 1].symbol == player_symbol:
            return True
    except:
        pass

    return False


def get_hot_cells_number(reshaped_board, player_symbol):
    hot_cells = 0
    for x, v in enumerate(reshaped_board):
        for y, token in enumerate(v):
            if is_hot_cell(reshaped_board, x, y, player_symbol):
                hot_cells += 1

    return hot_cells


def is_legal(movements, action_num, reshaped_board, symbol, has_started,
             remaining_pieces):
    if action_num == 2200:
        return 0
    movement = movements[action_num]
    square, piece_id, piece_super_id, grid = movement
    x, y = int(square / 10), square % 10
    if piece_super_id in remaining_pieces:  # El jugador posee la ficha
        for coordinates in grid:  # Chequeo casilla en blanco
            coord_x, coord_y = coordinates
            try:
                if (x + coord_x) < 0 or (y + coord_y) < 0 or (
                        x + coord_x) >= 10 or (
                        y + coord_y) >= 10:
                    return 0
                if reshaped_board[x + coord_x][y + coord_y].number != 0:
                    return 0
            except:
                return 0
        for coordinates in grid:  # Chequeo adyacentes diferentes al color del jugador
            coord_x, coord_y = coordinates
            """
            CASILLA DE DEBAJO
            """
            if (x + coord_x + 1) < 0 or (y + coord_y) < 0 or (
                    x + coord_x + 1) >= 10 or (
                    y + coord_y) >= 10:
                pass
            else:
                if reshaped_board[x + coord_x + 1][
                    y + coord_y].symbol == symbol:
                    return 0
            """
            CASILLA DE ARRIBA
            """
            if (x + coord_x - 1) < 0 or (y + coord_y) < 0 or (
                    x + coord_x - 1) >= 10 or (
                    y + coord_y) >= 10:
                pass
            else:
                if reshaped_board[x + coord_x - 1][
                    y + coord_y].symbol == symbol:
                    return 0

            """
            CASILLA DE LA DERECHA
            """
            if (x + coord_x) < 0 or (y + coord_y + 1) < 0 or (
                    x + coord_x) >= 10 or (
                    y + coord_y + 1) >= 10:
                pass
            else:
                if reshaped_board[x + coord_x][
                    y + coord_y + 1].symbol == symbol:
                    return 0

            """
            CASILLA DE LA IZQUIERDA
            """
            if (x + coord_x) < 0 or (y + coord_y - 1) < 0 or (
                    x + coord_x) >= 10 or (
                    y + coord_y - 1) >= 10:
                pass
            else:
                if reshaped_board[x + coord_x][
                    y + coord_y - 1].symbol == symbol:
                    return 0

        if not has_started:  # Primera pieza que coloca el jugador
            for coordinates in grid:
                coord_x, coord_y = coordinates
                if symbol == "b" and x + coord_x == 0 and y + coord_y == 0:  # PLAYER 1
                    return 1
                elif symbol == "g" and x + coord_x == 0 and y + coord_y == 9:  # PLAYER 2
                    return 1
                elif symbol == "r" and x + coord_x == 9 and y + coord_y == 9:  # PLAYER 3
                    return 1
                elif symbol == "y" and x + coord_x == 9 and y + coord_y == 0:  # PLAYER 4
                    return 1
            return 0

        for coordinates in grid:  # Chequeo alguna diagonal del color del jugador (hot cells)
            # logger.debug("Comprobando las hotcells")
            coord_x, coord_y = coordinates
            try:
                if reshaped_board[x + coord_x + 1][
                    y + coord_y + 1].symbol == symbol:
                    return 1

            except:

                pass
            try:
                if (x + coord_x - 1) >= 0 and \
                        reshaped_board[x + coord_x - 1][
                            y + coord_y + 1].symbol == symbol:
                    return 1
            except:
                pass
            try:
                if (y + coord_y - 1) >= 0 and \
                        reshaped_board[x + coord_x + 1][
                            y + coord_y - 1].symbol == symbol:
                    return 1
            except:
                pass
            try:
                if (y + coord_y - 1) >= 0 and (x + coord_x - 1) >= 0 and \
                        reshaped_board[x + coord_x - 1][
                            y + coord_y - 1].symbol == symbol:
                    return 1
            except:
                pass
    else:
        return 0
    return 0


def print_board(reshaped_board):
    printable_board = np.array([[y.symbol for y in x] for x in reshaped_board])
    colors = {
        ".": None,
        "b": "blue",
        "g": "green",
        "r": "red",
        "y": "yellow"
    }
    for i in range(0, 10):
        print(
            ' '.join([colored(x, colors[x]) for x in printable_board[i]]))


def get_posible_actions(movements, reshaped_board, symbol, has_started,
                               remaining_pieces):
    legal_actions = []
    for action_num in range(2201):
        legal = is_legal(movements, action_num, reshaped_board, symbol,
                         has_started, remaining_pieces)
        legal_actions.append(legal)
    if all(item == 0 for item in legal_actions):
        legal_actions[2200] = 1
    return legal_actions


def get_posible_actions_number(movements, reshaped_board, symbol, has_started,
                               remaining_pieces):
    legal_actions = get_posible_actions(movements, reshaped_board, symbol, has_started,
                        remaining_pieces)

    return sum(legal_actions)

def put_piece_in_board(movements, board, player, action_num):
    reshaped_board = copy.deepcopy(board)
    movement = movements[action_num]
    square, piece_id, piece_super_id, grid = movement
    x, y = int(square / 10), square % 10

    for coordinates in grid:
        coord_x, coord_y = coordinates
        reshaped_board[x + coord_x][
            y + coord_y] = player.token
    remaining_pieces = copy.deepcopy(player.super_id_pieces)
    remaining_pieces.remove(piece_super_id)

    return reshaped_board, remaining_pieces

def has_started(board, symbol):
    for x in board:
        for y in x:
            if y.symbol == symbol:
                return True
    return False

def score_actions(movements, new_board, player, player_has_started, player_rem_pieces):
    p_legal_actions = get_posible_actions(movements, new_board, player.symbol,
                                           player_has_started, player_rem_pieces)

    for act_p1, leg in enumerate(p_legal_actions):
        if leg == 1:
            board_p, rem_pieces_p = put_piece_in_board(movements, new_board,
                                                         player, act_p1)
            n = get_posible_actions_number(movements, board_p, player.symbol, True,
                                           rem_pieces_p)
            p_legal_actions[act_p1] = n
            del board_p, rem_pieces_p

    return p_legal_actions


def greedy_score(movements, action_num, board, players, current_player_num, w0, w1):
    player = players[current_player_num]
    new_board, remaining_pieces = put_piece_in_board(movements, board, player, action_num)
    other_players = [
        (current_player_num + 1) % 4,
        (current_player_num + 2) % 4,
        (current_player_num + 3) % 4,
    ]
    square, piece_id, piece_super_id, grid = movements[action_num]
    size = len(grid)
    p0 = get_posible_actions_number(movements, new_board, player.token.symbol, True, remaining_pieces)
    p1 = get_posible_actions_number(movements, new_board, players[other_players[0]].token.symbol, True,
                                    players[other_players[0]].super_id_pieces)
    p2 = get_posible_actions_number(movements, new_board,
                                    players[other_players[1]].token.symbol, True,
                                    players[other_players[1]].super_id_pieces)
    p3 = get_posible_actions_number(movements, new_board,
                                    players[other_players[2]].token.symbol, True,
                                    players[other_players[2]].super_id_pieces)

    score = w0*size + w1*(p0-sum([p1, p2, p3])/3)
    return score


def get_possible_actions_score(movements, action_num, board, current_player_num, players, best_cut=5):
    players_order = [
        current_player_num,
        (current_player_num + 1) % 4,
        (current_player_num + 2) % 4,
        (current_player_num + 3) % 4,
    ]
    scores = []
    # Current player
    board_p0, remaining_pieces_p0 = put_piece_in_board(movements, board, players[current_player_num], action_num)

    score = 0
    #next player p1
    p1 = players[players_order[1]]
    p1_legal_actions= score_actions(movements, board_p0, p1)

    best_p1 = sorted(range(len(p1_legal_actions)), key=lambda i: p1_legal_actions[i])[-best_cut:]

    for play_p1 in best_p1:
        # next player p2
        if p1_legal_actions[play_p1] != 0:
            p2 = players[players_order[2]]
            board_p1, remaining_pieces_p1 = put_piece_in_board(movements, board_p0, p1, play_p1)
            p2_legal_actions = score_actions(movements, board_p1, p2)

            best_p2 = sorted(range(len(p2_legal_actions)),
                             key=lambda i: p2_legal_actions[i])[-best_cut:]

            for play_p2 in best_p2:
                # next player p3
                if p2_legal_actions[play_p2] != 0:
                    p3 = players[players_order[3]]
                    board_p2, remaining_pieces_p2 = put_piece_in_board(movements, board_p1, p2, play_p2)
                    p3_legal_actions = score_actions(movements, board_p2, p3)

                    best_p3 = sorted(range(len(p3_legal_actions)),
                                     key=lambda i: p3_legal_actions[i])[-best_cut:]



                    for play_p3 in best_p3:
                        #player 0 again
                        if p3_legal_actions[play_p3] != 0:
                            p0 = players[players_order[0]]
                            board_p3, remaining_pieces_p3 = put_piece_in_board(movements, board_p2, p3, play_p3)
                            p0_legal_actions = score_actions(movements, board_p3, p0)











