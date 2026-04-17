import tkinter as tk
import random
from tkinter import messagebox

class MinesweeperGUI:
    def __init__(self, root, size=5, mines=5):
        self.root = root
        self.size = size
        self.mines = mines
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.visible = [[False for _ in range(size)] for _ in range(size)]
        self.mine_positions = set()

        self._place_mines()
        self._calculate_numbers()
        self._create_widgets()

    def _place_mines(self):
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            self.mine_positions.add((r, c))
            self.board[r][c] = '*'

    def _calculate_numbers(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '*':
                    continue
                count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        nr, nc = r + i, c + j
                        if 0 <= nr < self.size and 0 <= nc < self.size:
                            if self.board[nr][nc] == '*':
                                count += 1
                self.board[r][c] = str(count)

    def _create_widgets(self):
        for r in range(self.size):
            for c in range(self.size):
                btn = tk.Button(self.root, text=" ", width=3, height=1,
                                command=lambda r=r, c=c: self.reveal(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def reveal(self, r, c):
        if (r, c) in self.mine_positions:
            self.buttons[r][c].config(text="*", bg="red")
            messagebox.showinfo("Game Over", "💥 BOOM! You hit a mine.")
            self._reveal_all()
            return

        self._reveal_recursive(r, c)

        if self.is_won():
            self._reveal_all()
            messagebox.showinfo("Congratulations", "🎉 You cleared the board!")

    def _reveal_recursive(self, r, c):
        if not (0 <= r < self.size and 0 <= c < self.size):
            return
        if self.visible[r][c]:
            return

        self.visible[r][c] = True
        self.buttons[r][c].config(text=self.board[r][c], relief=tk.SUNKEN)

        if self.board[r][c] == '0':
            self.buttons[r][c].config(text=" ")
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self._reveal_recursive(r + i, c + j)

    def _reveal_all(self):
        for r in range(self.size):
            for c in range(self.size):
                self.buttons[r][c].config(text=self.board[r][c])

    def is_won(self):
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in self.mine_positions and not self.visible[r][c]:
                    return False
        return True


def main():
    root = tk.Tk()
    root.title("Minesweeper")
    size = 8   # You can change board size
    mines = 10 # You can change number of mines
    MinesweeperGUI(root, size, mines)
    root.mainloop()


if __name__ == "__main__":
    main()