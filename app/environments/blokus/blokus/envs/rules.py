import numpy as np
from termcolor import colored


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


def get_posible_actions_number(movements, reshaped_board, symbol, has_started,
                               remaining_pieces):
    legal_actions = []
    for action_num in range(2201):
        legal = is_legal(movements, action_num, reshaped_board, symbol,
                         has_started, remaining_pieces)
        legal_actions.append(legal)
    if all(item == 0 for item in legal_actions):
        legal_actions[2200] = 1

    return sum(legal_actions)
