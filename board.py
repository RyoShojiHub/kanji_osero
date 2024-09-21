import os
import random

EMPTY = 0
BLACK = 1
WHITE = 2


class Board(object):
    def __init__(self):
        self.board = self.initialize_board()
        self.kanji_list = self.load_kanji_readings()
        self.kanji_board = self.initialize_kanji_board()

    def initialize_board(self):
        """盤面を初期化する"""
        # 8*8の盤面を初期化
        board = [[EMPTY for i in range(8)] for _ in range(8)]
        # 中央に初期配置
        board[3][3], board[4][4] = BLACK, BLACK
        board[3][4], board[4][3] = WHITE, WHITE
        return board

    def load_kanji_readings(self):
        """漢字とその読みをテキストファイルから読み込む"""
        kanji_list = []
        try:
            with open('select_file.txt', 'r') as f:
                file_path = os.path.join('kanji_folder', f.readline().strip())
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    kanji, readings = line.strip().split()
                    reading_list = readings.split(',')
                    kanji_list.append((kanji, reading_list))
        except Exception as e:
            print(f"エラー: {e}")
            return None
        return kanji_list

    def initialize_kanji_board(self):
        """漢字の盤面を初期化する"""
        kanji_board = [[None for _ in range(8)] for _ in range(8)]
        random.shuffle(self.kanji_list)  # ランダムにシャッフル
        idx = 0
        for y in range(8):
            for x in range(8):
                kanji_board[y][x] = self.kanji_list[idx]
                idx += 1
        return kanji_board

    def set_stone(self, x, y, player):
        """石を置く"""
        self.board[y][x] = player

    def get_stone(self, x, y):
        """石の情報を取得する"""
        return self.board[y][x]

    def display_board(self):
        for y in self.board:
            print(y)
