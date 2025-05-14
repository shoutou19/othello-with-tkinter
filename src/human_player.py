import tkinter as tk
from board import Board
from player import Player
GRID_SIZE = 8
BLACK_TURN = 0
WHITE_TURN = 1
BLACK = 0
WHITE = 1

class HumanPlayer(Player):
    def __init__(self, color: int):
        self.color = color

    def get_position(self, event: tk.Event, board: Board) -> int:
        legal_board = board.get_legal_board()[self.color]
        while True:
            try:
                y = event.y // 50
                x = event.x // 50
                position = 1 << (y + x * GRID_SIZE)
                if legal_board & position:
                    return position
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input format.")
