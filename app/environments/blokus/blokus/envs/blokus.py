import gym
import copy
import numpy as np
from blokus.envs.constants import simple_pieces
import config

from stable_baselines import logger


def all_moves(num_squares):
    moves = []
    for i in range(num_squares):
        for j in simple_pieces:
            moves.append([i] + j)
    return moves

class Piece():
    def __init__(self, id, super_id, matrix):
        self.id = id
        self.super_id = super_id
        self.matrix = matrix


class Token():
    def __init__(self, symbol, number):
        self.number = number
        self.symbol = symbol


class Player():
    def __init__(self, id, token, pieces_super_id_list, has_started=False):
        self.id = id
        self.token = token
        self.pieces = pieces_super_id_list
        self.super_id_pieces = [p.super_id for p in self.pieces]
        self.partial_points = 0
        self.eliminated = False
        self.has_started = has_started


class BlokusEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False, manual=False):
        super(BlokusEnv, self).__init__()
        self.name = 'Blokus'
        self.manual = manual

        self.rows = 10
        self.cols = 10
        self.n_players = 4
        self.n_pieces = 21  # REVISAR
        self.grid_shape = (self.rows, self.cols)
        self.num_squares = self.rows * self.cols
        self.action_space = gym.spaces.Discrete(len(all_moves(self.num_squares)))
        self.observation_space = gym.spaces.Box(-1, 1, self.grid_shape + (self.n_players,))
        self.verbose = verbose

    @property
    def observation(self):
        player = self.current_player_num
        position_1 = np.array([1 if x.number == player + 1 else 0 for x in self.board]).reshape(self.grid_shape)
        position_2 = np.array([1 if x.number == ((player + 1) % 4) + 1 else 0 for x in self.board]).reshape(
            self.grid_shape)
        position_3 = np.array([1 if x.number == ((player + 2) % 4) + 1 else 0 for x in self.board]).reshape(
            self.grid_shape)
        position_4 = np.array([1 if x.number == ((player + 3) % 4) + 1 else 0 for x in self.board]).reshape(
            self.grid_shape)
        # TODO Agregar mas información (como por ejemplo hotcells)
        # position_5 = np.array([self.can_be_placed(i) for i, x in enumerate(self.board)]).reshape(self.grid_shape)

        out = np.stack([position_1, position_2, position_3, position_4, ], axis=-1)
        return out

    @property
    def legal_actions(self):
        legal_actions = []
        logger.debug(f"Numero de jugadas:{self.action_space.n}")
        for action_num in range(self.action_space.n):
            legal = self.is_legal(action_num)
            legal_actions.append(legal)

        return np.array(legal_actions)

    def is_legal(self, action_num):
        reshaped_boar = np.array(self.board).reshape(self.grid_shape)
        movements = all_moves(self.num_squares)
        movement = movements[action_num]
        square, piece_id, piece_super_id, grid = movement
        x, y = int(square / self.rows), square % self.cols
        #logger.debug(f"\n\n\nComprobando que el jugador pose la pieza {piece_super_id}")
        # logger.debug(f"Las piezas del jugador {self.players[self.current_player_num].super_id_pieces}")
        if piece_super_id in self.players[self.current_player_num].super_id_pieces: #El jugador posee la ficha
            # logger.debug(f"Comprobando que el jugador pose la pieza {piece_super_id}")
            for coordinates in grid:  # Chequeo casilla en blanco
                coord_x, coord_y = coordinates
                if action_num == 2178:
                    #logger.debug(f"Coordenadas : {x+coord_x}, {y+coord_y}")
                try:
                    #logger.debug(f"Coordenadas : {x+coord_x}, {y+coord_y}")
                    if (x + coord_x) < 0 or (y + coord_y) < 0 or (x + coord_x) > self.rows or (y + coord_y) > self.cols:
                        return 0
                    if reshaped_boar[x + coord_x][y + coord_y].number != 0:
                        return 0
                except:
                    return 0
            for coordinates in grid:  # Chequeo adyacentes diferentes al color del jugador
                coord_x, coord_y = coordinates
                try:
                    if reshaped_boar[x + coord_x + 1][y + coord_y].number == self.current_player.token.number:
                        return 0
                except:
                    continue
                try:
                    if reshaped_boar[x + coord_x - 1][y + coord_y].number == self.current_player.token.number:
                        return 0
                except:
                    continue
                try:
                    if reshaped_boar[x + coord_x][y + coord_y + 1].number == self.current_player.token.number:
                        return 0
                except:
                    continue
                try:
                    if reshaped_boar[x + coord_x + 1][y + coord_y - 1].number == self.current_player.token.number:
                        return 0
                except:
                    continue
            if not self.players[self.current_player_num].has_started:  # Primera pieza que coloca el jugador
                for coordinates in grid:
                    coord_x, coord_y = coordinates
                    if action_num == 2178:
                        #logger.debug(f"Primera jugada: simbolo {self.current_player.token.symbol}")
                        #logger.debug(f"Comprobando que {x + coord_x} = {self.rows -1} y que {y + coord_y} == 0")
                    if self.current_player.token.symbol == "b" and x + coord_x == 0 and y + coord_y == 0:
                        return 1
                    elif self.current_player.token.symbol == "g" and x + coord_x == self.rows - 1 and y + coord_y == 0:
                        return 1
                    elif self.current_player.token.symbol == "r" and x + coord_x == 0 and y + coord_y == self.cols - 1:
                        return 1
                    elif self.current_player.token.symbol == "y" and x + coord_x == self.rows - 1 and y + coord_y == self.cols - 1:
                        return 1
                return 0

            for coordinates in grid:# Chequeo alguna diagonal del color del jugador (hot cells)
                logger.debug("Comprobando las hotcells")
                try:
                    if reshaped_boar[x + coord_x + 1][y + coord_y + 1].number == self.current_player.token.number:
                        return 1
                except:
                    continue
                try:
                    if reshaped_boar[x + coord_x - 1][y + coord_y + 1].number == self.current_player.token.number:
                        return 1
                except:
                    continue
                try:
                    if reshaped_boar[x + coord_x + 1][y + coord_y - 1].number == self.current_player.token.number:
                        return 1
                except:
                    continue
                try:
                    if reshaped_boar[x + coord_x - 1][y + coord_y - 1].number == self.current_player.token.number:
                        return 1
                except:
                    continue
        else:
            return 0

        return 0

    def square_is_player(self, board, square, player):
        return board[square].number == self.players[player].token.number

    def check_game_over(self, board=None, player=None):

        reward = [0] * self.n_players

        if board is None:
            board = self.board

        if player is None:
            player = self.current_player_num

        for i_player in range(self.n_players):
            if i_player != self.current_player_num:
                if not self.players[i_player].eliminated:
                    if self.legal_actions.size == 0:
                        self.players[self.current_player_num].eliminated = True
                    return reward, False

        if self.legal_actions.size == 0:
            points = [p.partial_points for p in self.players]
            winner = np.argmax(points)
            reward = copy.deepcopy(points)
            for i in range(len(reward)):
                if i != winner:
                    new_reward = reward[i] - max(points)
                    reward[i] = new_reward

            return reward, True

        # if self.turns_taken == self.num_squares:
        #     logger.debug("Board full")
        #     return reward, True

        return reward, False  # -0.01 here to encourage choosing the win?

    @property
    def current_player(self):
        # TODO
        return self.players[self.current_player_num]

    def step(self, action):
        reward = [0] * self.n_players
        done = False

        # check move legality
        board = self.board

        if not self.players[self.current_player_num].eliminated:

            if not self.is_legal(action):
                done = True
                reward = [1] * self.n_players
                reward[self.current_player_num] = -1
            else:
                reshaped_boar = np.array(self.board).reshape(self.grid_shape)
                movements = all_moves(self.num_squares)
                movement = movements[action]
                square, piece_id, piece_super_id, grid = movement
                x, y = int(square / self.rows), square % self.cols

                for coordinates in grid:
                    coord_x, coord_y = coordinates
                    reshaped_boar[x + coord_x][y + coord_y] = self.current_player.token
                self.board = reshaped_boar.reshape(self.num_squares).tolist()

                self.turns_taken += 1
                reward, done = self.check_game_over()
        self.done = done
        self.players[self.current_player_num].has_started = True

        if not done:
            self.current_player_num = (self.current_player_num + 1) % self.n_players

        return self.observation, reward, done, {}

    def reset(self):
        self.board = [0] * self.num_squares
        self.board = [Token('.', 0)] * self.num_squares
        # self.board[0] = [Token('b', 5)]
        # self.board[self.cols - 1] = [Token('g', 6)]
        # self.board[self.num_squares - self.cols - 1] = [Token('r', 7)]
        # self.board[-1] = [Token('y', 8)]

        pieces = [Piece(*i) for i in simple_pieces]
        self.players = [Player(0, Token('b', 1), copy.deepcopy(pieces)),
                        Player(1, Token('g', 2), copy.deepcopy(pieces)),
                        Player(2, Token('r', 3), copy.deepcopy(pieces)),
                        Player(3, Token('y', 4), copy.deepcopy(pieces))]
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation

    def render(self, mode='human', close=False):
        # TODO
        logger.debug('')
        if close:
            return
        if self.done:
            logger.debug(f'GAME OVER')
        else:
            printable_board = np.array([x.symbol for x in self.board]).reshape(self.grid_shape)
            for i in range(0, self.rows):
                logger.debug(' '.join([x for x in printable_board[i]]))

        if self.verbose:
            logger.debug(f'\nObservation: \n{self.observation}')

        if not self.done:
            legal_actions = [i for i, o in enumerate(self.legal_actions) if o == 1]
            logger.debug(f'\nLegal actions: {legal_actions}')

    def rules_move(self):
        # TODO
        WRONG_MOVE_PROB = 0.01
        player = self.current_player_num

        for action in range(self.action_space.n):
            if self.is_legal(action):
                new_board = self.board.copy()
                square = self.get_square(new_board, action)
                new_board[square] = self.players[player].token
                _, done = self.check_game_over(new_board, player)
                if done:
                    action_probs = [WRONG_MOVE_PROB] * self.action_space.n
                    action_probs[action] = 1 - WRONG_MOVE_PROB * (self.action_space.n - 1)
                    return action_probs

        player = (self.current_player_num + 1) % 2

        for action in range(self.action_space.n):
            if self.is_legal(action):
                new_board = self.board.copy()
                square = self.get_square(new_board, action)
                new_board[square] = self.players[player].token
                _, done = self.check_game_over(new_board, player)
                if done:
                    action_probs = [0] * self.action_space.n
                    action_probs[action] = 1 - WRONG_MOVE_PROB * (self.action_space.n - 1)
                    return action_probs

        action, masked_action_probs = self.sample_masked_action([1] * self.action_space.n)
        return masked_action_probs
