from board import Board
from player import Player
import copy

GRID_SIZE = 8
BLACK_TURN = 0
WHITE_TURN = 1
BLACK = 0
WHITE = 1

class NegamaxPlayer(Player):
    weight = [
        2714, 147, 69, -18, -18, 69, 147, 2714,
        147, -577, -186, -153, -153, -186, -577, 147,
        69, -186, -379, -122, -122, -379, -186, 69,
        -18, -153, -122, -169, -169, -122, -153, -18,
        -18, -153, -122, -169, -169, -122, -153, -18,
        69, -186, -379, -122, -122, -379, -186, 69,
        147, -577, -186, -153, -153, -186, -577, 147,
        2714, 147, 69, -18, -18, 69, 147, 2714
    ]


    def __init__(self, color: int, depth: int):
        self.color = color
        self.depth = depth
    
    def negaMax(self, board: Board, depth: int, passed: bool) -> int:
        if depth == 0:
            return self.evaluate(board)
        
        legal_board = board.get_legal_board()[self.color]

        if legal_board == 0:
            if passed:
                return 0
            else:
                return -self.negaMax(board, depth, True)

        max_score = float('-inf')
        for i in range(GRID_SIZE * GRID_SIZE):
            if legal_board & (1 << i):
                new_board = copy.deepcopy(board)
                new_board.flip(self.color, i)
                score = -self.negaMax(new_board, depth - 1, False)
                max_score = max(max_score, score)

        return max_score
    
    def evaluate(self, board: Board) -> int:
        score = 0
        my_board = board.get_board()[self.color]
        opponent_board = board.get_board()[self.color ^ 1]
        for i in range(GRID_SIZE * GRID_SIZE):
            if my_board & (1 << i):
                score += self.weight[i]
            if opponent_board & (1 << i):
                score -= self.weight[i]
        return score

    def get_position(self, board: Board) -> int:
        legal_board = board.get_legal_board()[self.color]
        best_move = 0
        best_score = float('-inf')

        for i in range(GRID_SIZE * GRID_SIZE):
            if legal_board & (1 << i):
                new_board = copy.deepcopy(board)
                new_board.flip(self.color, i)
                score = -self.negaMax(new_board, self.depth - 1, False)
                if score > best_score:
                    best_score = score
                    best_move = i

        return 1 << best_move