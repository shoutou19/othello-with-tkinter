import random
from board import Board
from player import Player
GRID_SIZE = 8
BLACK_TURN = 0
WHITE_TURN = 1
BLACK = 0
WHITE = 1

class RandomPlayer(Player):
    def __init__(self, color: int):
        self.color = color

    def get_position(self, board: Board) -> int:
        legal_board = board.get_legal_board()[self.color]
        legal_moves = [1 << i for i in range(GRID_SIZE * GRID_SIZE) if legal_board & (1 << i)]
        if legal_moves:
            return random.choice(legal_moves)
        else:
            return 0
        