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
        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.game.board.display_board()

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

        if self.game.place_stone(x, y):
            self.update_display()
            if self.game.pass_check():
                messagebox.showinfo("パス", "プレイヤーがパスしました")


    def update_display(self):
        """表示を更新"""
        self.canvas.delete("all")
        self.draw_board()
