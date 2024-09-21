import tkinter

import game
import gui


def main():
    root = tkinter.Tk()
    root.resizable(height=False, width=False)
    gm = game.Game()
    ui = gui.Gui(root, gm)
    root.mainloop()


if __name__ == '__main__':
    main()
