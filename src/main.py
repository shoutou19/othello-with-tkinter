import tkinter as tk

from board import Board
from player import Player
from human_player import HumanPlayer
from random_player import RandomPlayer
from negamax_player import NegamaxPlayer

GRID_SIZE = 8
BLACK_TURN = 0
WHITE_TURN = 1
BLACK = 0
WHITE = 1

def draw_board(canvas, rows=8, cols=8, cell_size=50):
    for row in range(rows):
        for col in range(cols):
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="green")

def draw_piece(canvas, board: Board, cell_size=50):
    for i in range(64):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        if board.black_board & (1 << i):
            canvas.create_oval(x1, y1, x2, y2, fill="black")
        elif board.white_board & (1 << i):
            canvas.create_oval(x1, y1, x2, y2, fill="white")

def draw_legal_moves(canvas, legal_board: int, cell_size=50):
    for i in range(64):
        if legal_board & (1 << i):
            row = i // GRID_SIZE
            col = i % GRID_SIZE
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_oval(x1, y1, x2, y2, outline="red", width=3)

def draw_scores(canvas, scores, cell_size=50):
    black_score, white_score = scores
    board_width = GRID_SIZE * cell_size
    board_height = GRID_SIZE * cell_size

    # スコアをボードの下に表示
    canvas.create_text(board_width // 2, board_height + 10, text=f"Black: {black_score}", fill="black", font=("Arial", 14))
    canvas.create_text(board_width // 2, board_height + 30, text=f"White: {white_score}", fill="black", font=("Arial", 14))

def draw_winner(canvas, scores):
    black_score, white_score = scores
    if black_score > white_score:
        winner = "Black"
    elif white_score > black_score:
        winner = "White"
    else:
        winner = "Draw"
    canvas.create_text(GRID_SIZE * 50 // 2, GRID_SIZE * 50 // 2, text=f"{winner} win!", font=("Arial", 24), fill="red")

class Game:
    def __init__(self, black_player: Player, white_player: Player):
        self.board = Board()
        self.turn = BLACK_TURN
        self.player = [black_player, white_player]
        self.root = None
        self.canvas = None
        self.clicked_position = None  # クリックされた位置を保持

    def on_canvas_click(self, event):
        # クリックされた位置をビット座標に変換
        row = event.y // 50
        col = event.x // 50
        position = 1 << (row * GRID_SIZE + col)
        legal_board = self.board.get_legal_board()[self.turn]
        if legal_board & position:  # 合法手か確認
            self.clicked_position = position

    def update_game(self):
        self.canvas.delete("all")
        draw_board(self.canvas)
        draw_piece(self.canvas, self.board)
        draw_legal_moves(self.canvas, self.board.get_legal_board()[self.turn])
        draw_scores(self.canvas, self.board.get_scores())

        scores = self.board.get_scores()
        legal_boards = self.board.get_legal_board()

        if legal_boards[BLACK] == 0 and legal_boards[WHITE] == 0:
            print("Game over")
            draw_winner(self.canvas, scores)
            self.root.after(2000, self.root.quit)  # 2秒後にウィンドウを閉じる
            return  # ゲーム終了
            

        if legal_boards[self.turn] == 0:
            print(f"Player {self.turn} has no legal moves. Skipping turn.")
            self.turn ^= 1
            self.root.after(100, self.update_game)
            return

        if isinstance(self.player[self.turn], HumanPlayer):
            # HumanPlayer の場合はクリックを待つ
            if self.clicked_position is None:
                self.root.after(100, self.update_game)
                return
            position = self.clicked_position
            self.clicked_position = None  # クリック位置をリセット
        else:
            position = self.player[self.turn].get_position(self.board)

        self.board.flip(self.turn, position)

        # ターンを切り替える
        self.turn ^= 1
        self.root.after(100, self.update_game)

    def main(self):
        self.root = tk.Tk()
        self.root.title("Othello Game")
        # キャンバスの高さをスコア表示分（50px）増やす
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE * 50, height=GRID_SIZE * 50 + 50)
        self.canvas.pack()

        # クリックイベントをバインド
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.update_game()  # ゲームの更新を開始
        self.root.mainloop()


if __name__ == "__main__":
    print("Welcome to Othello!")

    player1 = HumanPlayer(BLACK)
    player2 = NegamaxPlayer(WHITE, 3)  # Example: Negamax player with depth 3

    game = Game(player1, player2)
    game.main()
    print("Game over")