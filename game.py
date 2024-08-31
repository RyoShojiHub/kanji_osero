import board

EMPTY = 0
BLACK = 1
WHITE = 2

class Game(object):
    def __init__(self):
        self.current_player = BLACK
        self.board = board.Board()
        self.score = {'black': 2, 'white': 2}

    def initialize_game(self):
        """ゲームを初期化する"""
        self.board.board = self.board.initialize_board()
        self.current_player = BLACK
        self.count_score()


    def switch_player(self):
        """手番を交代する"""
        self.current_player = BLACK if self.current_player == WHITE else WHITE


    def is_valid_move(self, x, y):
        """指定された場所に石を置けるか検証"""
        if self.board.get_stone(x, y) != EMPTY:
            return False

        # チェックで使う方向差分用の配列
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            if self.check_direction(x, y, dx, dy):
                return True
        return False


    def check_direction(self, x, y, dx,dy):
        """石を反転させられるかチェック"""
        x += dx
        y += dy
        found_opponent = False
        while 0 <= x < 8 and 0 <= y < 8:
            stone = self.board.get_stone(x,y)
            if stone == EMPTY:
                return False
            if stone == self.current_player:
                if found_opponent:
                    return True
                else:
                    return False
            found_opponent = True
            x += dx
            y += dy
        return False


    def place_stone(self, x, y):
        """石を置き、必要に応じて反転する"""
        if not self.is_valid_move(x, y):
            return False

        self.board.set_stone(x, y, self.current_player)

        # チェックで使う方向差分用の配列
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            if self.check_direction(x, y, dx, dy):
                x2, y2 = x + dx, y + dy
                flip_positions
                while 0 <= x < 8 and 0 <= y < 8 and self.board.get_stone(x2, y2) != self.current_player:
                    self.board.set_stone(x, y, self.current_player)
                    x2 += dx
                    y2 += dy

        self.count_score()
        self.switch_player()
        return True


    def count_score(self):
        """石の数をそれぞれカウントする"""
        black = sum(row.count(BLACK) for row in self.board.board)
        white = sum(row.count(WHITE) for row in self.board.board)
        self.score['black'] = black
        self.score['white'] = white


    def pass_check(self):
        """パスかどうかチェックする"""
        is_pass = True
        for y in range(8):
            for x in range(8):
                if self.is_valid_move(x, y):
                    return False
        if is_pass:
            self.switch_player()
            return True
