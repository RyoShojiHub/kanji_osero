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

    def check_reading(self, x, y, reading_input):
        """漢字の読みが正しいかチェック"""
        correct_readings = self.board.kanji_board[y][x][1]
        return reading_input in correct_readings

    def switch_player(self):
        """手番を交代する"""
        self.current_player = BLACK if self.current_player == WHITE else WHITE

    def is_valid_move(self, x, y, player=None):
        """指定された場所に石を置けるか検証"""
        if player is None:
            player = self.current_player
        if self.board.get_stone(x, y) != EMPTY:
            return False

        # チェックで使う方向差分用の配列
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            found_opponent_stone = False
            current_x, current_y = x + dx, y + dy
            while 0 <= current_x < 8 and 0 <= current_y < 8:
                stone = self.board.get_stone(current_x, current_y)
                if stone == EMPTY:
                    break
                if stone != player:  # 相手の石の場合
                    found_opponent_stone = True
                else:  # 自分の石が見つかった場合
                    if found_opponent_stone:
                        return True
                    else:
                        break
                current_x, current_y = current_x + dx, current_y + dy
        return False

    def check_direction(self, x, y, dx, dy):
        """反転できる石のリストを返す"""
        current_x, current_y = x + dx, y + dy
        stone_to_flip = []
        confirmed_stones = []
        while 0 <= current_x < 8 and 0 <= current_y < 8:
            stone = self.board.get_stone(current_x, current_y)
            if stone == EMPTY:
                return confirmed_stones

            if stone == self.current_player:
                confirmed_stones = stone_to_flip
                return confirmed_stones
            stone_to_flip.append((current_x, current_y))  # 反転する石の候補
            current_x, current_y = current_x + dx, current_y + dy
        return confirmed_stones

    def place_stone(self, x, y):
        """石を置き、必要に応じて反転する"""
        # if not self.is_valid_move(x, y):
        #     return False

        self.board.set_stone(x, y, self.current_player)

        # チェックで使う方向差分用の配列
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            stone_to_flip = self.check_direction(x, y, dx, dy)
            for flip_x, flip_y in stone_to_flip:
                self.board.set_stone(flip_x, flip_y, self.current_player)

        self.count_score()
        return True

    def count_score(self):
        """石の数をそれぞれカウントする"""
        black_score = sum(row.count(BLACK) for row in self.board.board)
        white_score = sum(row.count(WHITE) for row in self.board.board)
        self.score['black'] = black_score
        self.score['white'] = white_score

    def winner(self):
        """勝者を返す"""
        if self.score['black'] < self.score['white']:
            return "白の勝ち"
        elif self.score['black'] > self.score['white']:
            return "黒の勝ち"
        else:
            return "引き分け"

    def pass_check(self):
        """パスかどうかチェックする"""
        for y in range(8):
            for x in range(8):
                if self.is_valid_move(x, y):
                    return False
        return True

    def can_player_move(self):
        """両方のプレイヤーが動けるか確認する"""
        players = [BLACK, WHITE]
        for player in players:
            for y in range(8):
                for x in range(8):
                    if self.is_valid_move(x, y, player):
                        return True
        return False
