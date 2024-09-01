import tkinter
from tkinter import messagebox

EMPTY = 0
BLACK = 1
WHITE = 2


class Gui(object):
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.canvas = tkinter.Canvas(root, width=1000, height=800)
        self.canvas.pack()
        self.root.title('オセロ')
        self.current_player_label = tkinter.Label(root, text='', font=("Arial", 14))
        self.current_player_label.pack()
        self.update_display()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        for y in range(8):
            for x in range(8):
                self.canvas.create_rectangle(x*80+60, y*80+60, x*80+140, y*80+140, fill='green')
                stone = self.game.board.get_stone(x, y)
                if stone == BLACK:
                    self.canvas.create_oval(x*80+60, y*80+60, x*80+140, y*80+140, fill='black')
                elif stone == WHITE:
                    self.canvas.create_oval(x*80+60, y*80+60, x*80+140, y*80+140, fill='white')

    def handle_click(self, event):
        """クリックイベントを処理"""
        x = (event.x - 60) // 80
        y = (event.y - 60) // 80

        if not (0 <= x < 8 and 0 <= y < 8):
            return

        if self.game.is_valid_move(x, y):
            self.game.place_stone(x, y)
            self.game.switch_player()
            self.update_display()
            self.update_current_player_display()

        if self.game.pass_check():
            messagebox.showinfo("パス", "プレイヤーがパスしました")

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