import numpy as np

simple_pieces = [[0, 1, np.array([[0, 0]])],
                 [1, 2, np.array([[0, 0], [1, 0]])],
                 [2, 2, np.array([[0, 0], [0, 1]])],
                 [3, 3, np.array([[0, 0], [1, 0], [2, 0]])],
                 [4, 3, np.array([[0, 0], [0, 1], [0, 2]])],
                 [5, 4, np.array([[0, 0], [1, 0], [1, 1]])],
                 [6, 4, np.array([[0, 0], [1, 0], [0, 1]])],
                 [7, 4, np.array([[0, 0], [0, 1], [1, 1]])],
                 [8, 4, np.array([[0, 0], [1, 0], [1, -1]])],
                 [9, 5, np.array([[0, 0], [1, 0], [2, 0], [3, 0]])],
                 [10, 5, np.array([[0, 0], [0, 1], [0, 2], [0, 3]])],
                 [11, 6, np.array([[0, 0], [1, 0], [2, 0], [2, -1]])],
                 [12, 6, np.array([[0, 0], [1, 0], [1, 1], [1, 2]])],
                 [13, 6, np.array([[0, 0], [0, 1], [1, 0], [2, 0]])],
                 [14, 6, np.array([[0, 0], [0, 1], [0, 2], [1, 2]])],
                 [15, 7, np.array([[0, 0], [1, 0], [1, 1], [2, 0]])],
                 [16, 7, np.array([[0, 0], [0, 1], [1, 1], [0, 2]])],
                 [17, 7, np.array([[0, 0], [1, 0], [1, -1], [2, 0]])],
                 [18, 7, np.array([[0, 0], [0, 1], [-1, 1], [0, 2]])],
                 [19, 8, np.array([[0, 0], [1, 0], [1, 1], [0, 1]])],
                 [20, 9, np.array([[0, 0], [0, 1], [1, 1], [1, 2]])],
                 [21, 9, np.array([[0, 0], [1, 0], [1, -1], [2, -1]])]]

def all_moves(num_squares):
    moves = []
    for i in range(num_squares):
        for j in simple_pieces:
            moves.append([i] + j)
    return moves


rows = 10
cols = 10

x = 4,
y = 4
for id, p in enumerate(simple_pieces):
    print(f"\n pieza {id}")
    board = np.array(["-"] * (rows * cols))
    board_reshaped = board.reshape((10, 10))
    grid = p[2]
    for coordinates in grid:
        coord_x, coord_y = coordinates
        board_reshaped[x+coord_x, y + coord_y] = "0"

    for i in range(0, rows):
        print(' '.join([x for x in board_reshaped[i]]))

pieza = int(input("Elige la pieza: "))

x = int(input("Elige la coordenada x: "))
y = int(input("Elige la coordenada y: "))

print(f"\n\nPieza elegida {pieza}")
square_elegido = 10*x + y
print(f"Cuadrado: {square_elegido}")
accion = -1
for id, move in enumerate(all_moves(rows*cols)):
    square, piece_id, piece_super_id, grid = move

    if piece_id == pieza and square_elegido == square:
        print(f"Accion elegida: {id}")
        accion = id

board = np.array(["-"] * (rows * cols))
board_reshaped = board.reshape((10, 10))
grid = simple_pieces[pieza][2]
for coordinates in grid:
    coord_x, coord_y = coordinates
    board_reshaped[x+coord_x, y + coord_y] = "0"
for i in range(0, rows):
    print(' '.join([x for x in board_reshaped[i]]))



