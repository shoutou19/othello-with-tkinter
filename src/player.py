from abc import ABCMeta, abstractmethod
from board import Board
GRID_SIZE = 8
BLACK_TURN = 0
WHITE_TURN = 1
BLACK = 0
WHITE = 1

class Player(metaclass=ABCMeta):
    def __init__(self, color: int):
        self.color = color

    @abstractmethod
    def get_position(self, board: Board) -> int:
        pass