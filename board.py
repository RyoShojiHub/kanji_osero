EMPTY = 0
BLACK = 1
WHITE = 2

class Board(object):
    def __init__(self):
        self.board = self.initialize_board()


    def initialize_board(self):
        """盤面を初期化する"""
        board = [[EMPTY for i in range(8)] for _ in range(8)]
        board[3][3], board[4][4] = BLACK, BLACK
        board[3][4], board[4][3] = WHITE, WHITE
        return board


    def set_stone(self, x, y, player):
        """石を置く"""
        self.board[y][x] = player


    def get_stone(self, x, y):
        """石の情報を取得する"""
        return self.board[x][y]


    def display_board(self):
        for y in self.board:
            print(y)


