GRID_SIZE = 8
BLACK_TURN = 0
WHITE_TURN = 1

class Board:
    def __init__(self):
        self.black_board = (
            0b00000000_00000000_00000000_00001000_00010000_00000000_00000000_00000000
        )
        self.white_board = (
            0b00000000_00000000_00000000_00010000_00001000_00000000_00000000_00000000
        )

    # # xy座標をビット位置に変換
    # def to_bit_position(self, x, y):
    #     return 1 << (x + y * GRID_SIZE)
    
    def get_scores(self):
        black_score = bin(self.black_board).count("1")
        white_score = bin(self.white_board).count("1")
        return black_score, white_score
    
    def get_board(self):
        return self.black_board, self.white_board
    
    # 合法手ボードを取得
    def get_legal_board(self):
        masks = [
            (1, 0x7E7E7E7E7E7E7E7E), #horizontal
            (7, 0x007E7E7E7E7E7E00), #every_side
            (8, 0x00FFFFFFFFFFFF00), #vartical
            (9, 0x007E7E7E7E7E7E00) #every_side
        ]
        shifts = [lambda x, n: x << n, lambda x, n: x >> n]
        legal_black_board, legal_white_board = 0, 0
        blank_board = ~(self.white_board | self.black_board)

        def culc_legal_board(player_board, opponent_board):
            legal_board = 0
            for n_shifts, mask in masks:
                for shift in shifts:
                    tmp_board = (shift(player_board, n_shifts) & opponent_board) & mask
                    for _ in range(5):
                        tmp_board |= (shift(tmp_board, n_shifts) & opponent_board) & mask
                    legal_board |= shift(tmp_board, n_shifts) & blank_board
            return legal_board

        legal_black_board = culc_legal_board(self.black_board, self.white_board)
        legal_white_board = culc_legal_board(self.white_board, self.black_board)

        return legal_black_board, legal_white_board
    

    # 裏返す
    def flip(self, turn, position):
        masks = [
            (9, 0xFEFEFEFEFEFEFE00),
            (8, 0xFFFFFFFFFFFFFF00),
            (7, 0x7F7F7F7F7F7F7F00),
            (1, 0xFEFEFEFEFEFEFEFE),
            (-1, 0x7F7F7F7F7F7F7F7F),
            (-7, 0x00FEFEFEFEFEFEFE),
            (-8, 0x00FFFFFFFFFFFFFF),
            (-9, 0x007F7F7F7F7F7F7F)
        ]
        shift = lambda x, n: x << n if n > 0 else x >> -n
        

        def get_flip_board(turn, position):
            rev = 0
            player_board = self.black_board if turn == BLACK_TURN else self.white_board
            opponent_board = self.white_board if turn == BLACK_TURN else self.black_board
            for n_shifts, mask in masks:
                tmp = 0
                pos = shift(position, n_shifts) & mask
                while (pos != 0) and ((pos & opponent_board) != 0):
                    tmp |= pos
                    pos = shift(pos, n_shifts) & mask
                if (pos & player_board) != 0:
                    rev |= tmp
            return rev
        
        rev = get_flip_board(turn, position)
        if turn == BLACK_TURN:
            self.black_board ^= position | rev
            self.white_board ^= rev
        else:
            self.white_board ^= position | rev
            self.black_board ^= rev
    
    def print_board(self):
        print("  " + " ".join(str(i) for i in range(GRID_SIZE)))
        for i in range(GRID_SIZE):
            print(i, end=" ")
            for j in range(GRID_SIZE):
                pos = 1 << (i + j * GRID_SIZE)
                if self.black_board & pos:
                    print("x", end=" ")
                elif self.white_board & pos:
                    print("o", end=" ")
                else:
                    print("-", end=" ")
            print()