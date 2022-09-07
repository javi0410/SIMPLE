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
    def __init__(self, id, token, pieces_super_id_list):
        self.id
        self.token = token
        self.pieces = pieces_super_id_list
        self.partial_points = 0
        self.eliminated = False


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
        self.action_space = gym.spaces.Discrete(self.n_pieces * self.num_squares)
        self.observation_space = gym.spaces.Box(-1, 1, self.grid_shape + (self.n_players,))
        self.verbose = verbose

    @property
    def observation(self):
        # TODO
        if self.current_player.token.number == 1:
            position_1 = np.array([1 if x.number == 1 else 0 for x in self.board]).reshape(self.grid_shape)
            position_2 = np.array([1 if x.number == -1 else 0 for x in self.board]).reshape(self.grid_shape)
            position_3 = np.array([self.can_be_placed(i) for i, x in enumerate(self.board)]).reshape(self.grid_shape)
        else:
            position_1 = np.array([1 if x.number == -1 else 0 for x in self.board]).reshape(self.grid_shape)
            position_2 = np.array([1 if x.number == 1 else 0 for x in self.board]).reshape(self.grid_shape)
            position_3 = np.array([self.can_be_placed(i) for i, x in enumerate(self.board)]).reshape(self.grid_shape)

        out = np.stack([position_1, position_2, position_3], axis=-1)
        return out

    @property
    def legal_actions(self):
        legal_actions = []
        for action_num in range(self.action_space.n):
            legal = self.is_legal(action_num)
            legal_actions.append(legal)

        return np.array(legal_actions)

    def is_legal(self, action_num):
        reshaped_boar = self.board.reshape(self.grid_shape)
        movements = all_moves(self.num_squares)
        movement = movements[action_num]
        square, piece_id, piece_super_id, grid = movement
        x, y = int(square / self.rows), square % self.cols
        if piece_super_id in self.players[self.current_player_num].pieces:
            for coordinates in grid:  # Chequeo casilla en blanco
                coord_x, coord_y = coordinates
                try:
                    if reshaped_boar[x + coord_x][y + coord_y].number != 0:
                        return 0
                except:
                    return 0
            for coordinates in grid:  # Chequeo ortogonales diferentes al color del jugador
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
            for coordinates in grid:  # Chequeo alguna diagonal del color del jugador (hot cells)
                coord_x, coord_y = coordinates
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
                if self.current_player.token.number == "b" and x + coord_x == 0 and y + coord_y == 0:
                    return 1
                elif self.current_player.token.number == "g" and x + coord_x == self.rows - 1 and y + coord_y == 0:
                    return 1
                elif self.current_player.token.number == "r" and x + coord_x == 0 and y + coord_y == self.cols - 1:
                    return 1
                elif self.current_player.token.number == "y" and x + coord_x == self.rows - 1 and y + coord_y == self.cols - 1:
                    return 1
                else:
                    return 0
        else:
            return 0

        return 1

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
                reshaped_boar = self.board.reshape(self.grid_shape)
                movements = all_moves(self.num_squares)
                movement = movements[action]
                square, piece_id, piece_super_id, grid = movement
                x, y = int(square / self.rows), square % self.cols

                for coordinates in grid:
                    coord_x, coord_y = coordinates
                    reshaped_boar[x + coord_x][y + coord_y] = self.current_player.token
                self.board = reshaped_boar.reshape(self.num_squares)

                self.turns_taken += 1
                r, done = self.check_game_over()
                reward = [-r, -r]
                reward[self.current_player_num] = r

        self.done = done

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
            legal_actions = [i for i, o in enumerate(self.legal_actions) if o != 0]

            logger.debug(f'\nLegal actions: {[i for i, o in enumerate(self.legal_actions) if o != 0]}')

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
