import tkinter
from tkinter import messagebox, simpledialog

EMPTY = 0
BLACK = 1
WHITE = 2
MAX_FAULT_COUNT = 3


class Gui(object):
    def __init__(self, root, game):
        self.root = root
        self.game = game  # Gameクラスのインスタンス
        self.canvas = tkinter.Canvas(self.root, width=1200, height=800)
        self.canvas.pack()
        self.root.title('漢字オセロ')

        self.game_over = False
        self.fault_count = 0

        self.current_player_label = tkinter.Label(self.root, text='', font=("Arial", 14))
        self.current_player_label.place(x=800, y=50)
        self.score_label = tkinter.Label(self.root, text='', font=("Arial", 14))
        self.score_label.place(x=800, y=90)
        self.fault_label = tkinter.Label(self.root,
                                         text=f'間違い: {self.fault_count}/{MAX_FAULT_COUNT}',
                                         font=("Arial", 14))
        self.fault_label.place(x=800, y=130)
        self.pass_button = tkinter.Button(self.root, text="パス", command=self.pass_turn, width=12, height=3, font=("Arial", 16))
        self.pass_button.place(x=800, y=200)
        self.giveup_button = tkinter.Button(self.root, text="ギブアップ\n(ゲーム終了)", command=self.give_up, width=12, height=3, font=("Arial", 16))
        self.giveup_button.place(x=1000, y=200)
        self.reset_button = tkinter.Button(self.root, text="ゲームリセット", command=self.reset_game, width=12, height=3, font=("Arial", 16))
        self.reset_button.place(x=900, y=600)

        self.update_display()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        """盤面の描画を行う"""
        for y in range(8):
            for x in range(8):
                self.canvas.create_rectangle(x*90+20, y*90+20, x*90+110, y*90+110, fill='green')
                stone = self.game.board.get_stone(x, y)
                if stone == BLACK:
                    self.canvas.create_oval(x*90+20, y*90+20, x*90+110, y*90+110, fill='black')
                elif stone == WHITE:
                    self.canvas.create_oval(x*90+20, y*90+20, x*90+110, y*90+110, fill='white')
                else:
                    kanji = self.game.board.kanji_board[y][x][0]
                    self.canvas.create_text(x*90+65, y*90+65, text=kanji, font=("Arial", 20))

    def handle_click(self, event):
        """クリックイベントを処理"""
        if self.game_over:
            return

        x = (event.x - 20) // 90
        y = (event.y - 20) // 90

        if not (0 <= x < 8 and 0 <= y < 8):
            return

        if self.game.is_valid_move(x, y):  # 石を置けるか検証
            # 漢字の読みを入力
            reading_input = simpledialog.askstring("読みを入力",
                                                   f'"{self.game.board.kanji_board[y][x][0]}"の読みをひらがなで入力してください\
                                                   \n(送り仮名まで入力してください):')
            # キャンセルされた場合
            if reading_input is None:
                return
            # 読みが正しいかチェック
            if self.game.check_reading(x, y, reading_input):
                self.game.place_stone(x, y)
                self.game.switch_player()
                self.update_display()
                self.fault_count = 0
                self.fault_label.config(text=f"間違い: {self.fault_count}/{MAX_FAULT_COUNT}")
            else:
                self.fault_count += 1
                if self.fault_count < MAX_FAULT_COUNT:  # 一定回数以上間違えた場合パス
                    messagebox.showinfo("間違い", f"間違いです。\n残り回数{3-self.fault_count}")
                    self.fault_label.config(text=f"間違い: {self.fault_count}/{MAX_FAULT_COUNT}")
                else:
                    messagebox.showinfo("パス", f"{self.fault_count}回間違えたため、相手の手番になります。")
                    self.game.switch_player()
                    self.update_display()
                    self.fault_count = 0
                    self.fault_label.config(text=f"間違い: {self.fault_count}/{MAX_FAULT_COUNT}")

        if not self.game.can_player_move():
            messagebox.showinfo("ゲームセット",
                                f"黒:{self.game.score['black']}  白:{self.game.score['white']}\
                                \n{self.game.winner()}")
            self.game_over = True

        if self.game.pass_check():
            messagebox.showinfo("パス", "プレイヤーがパスしました")
            self.game.switch_player()
            self.update_display()

    def pass_turn(self):
        """プレイヤーがパスを選択した場合"""
        if self.game_over:
            return
        messagebox.showinfo("パス", "プレイヤーがパスしました")
        self.game.switch_player()  # プレイヤーを交代
        self.update_display()

    def give_up(self):
        """プレイヤーがギブアップを選択した場合"""
        if self.game_over:
            return
        messagebox.showinfo("ギブアップ", f"プレイヤーがギブアップしました。\
        \n黒:{self.game.score['black']}  白:{self.game.score['white']}\
        \n{self.game.winner()}")
        self.game_over = True

    def reset_game(self):
        """リセットボタンを押したときにゲームをリセットする"""
        self.game.reset_game()
        self.game_over = False
        self.fault_count = 0
        self.update_display()

    def update_display(self):
        """表示を更新"""
        self.canvas.delete("all")
        self.draw_board()
        self.update_current_player_display()

    def update_current_player_display(self):
        """現在のプレイヤー表示を更新"""
        if self.game.current_player == BLACK:
            player_text = "現在のプレイヤー: 黒"
        else:
            player_text = "現在のプレイヤー: 白"
        self.current_player_label.config(text=player_text)

        score_text = f"黒の石: {self.game.score['black']}  白の石: {self.game.score['white']}"
        self.score_label.config(text=score_text)
