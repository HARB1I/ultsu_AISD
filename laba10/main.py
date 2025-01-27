import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.center_window(490, 400)
        self.game_board = [[None, None, None], [None, None, None], [None, None, None]]  # создание поле 3x3
        self.current_player = "X" # игрок будет начинать с X
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text="", font=('Arial', 40), width=5, height=2,
                                   command=lambda r=row, c=col: self.player_move(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def player_move(self, row, col):
        if self.game_board[row][col] is None:
            self.game_board[row][col] = "X"
            self.buttons[row][col].config(text="X", state=tk.DISABLED)
            if self.check_winner("X"):
                messagebox.showinfo("Победа!", "Поздравляем, вы выиграли! (но этого не должно было случиться!)")
                self.reset_board()
            elif self.check_tie():
                messagebox.showinfo("Ничья", "Ничья!")
                self.reset_board()
            else:
                self.ai_move()

    def ai_move(self):
        move = self.find_best_move()
        if move:
            row, col = move
            self.game_board[row][col] = "O"
            self.buttons[row][col].config(text="O", state=tk.DISABLED)
            if self.check_winner("O"):
                messagebox.showinfo("Поражение", "Робот победил!")
                self.reset_board()
            elif self.check_tie():
                messagebox.showinfo("Ничья", "Ничья!")
                self.reset_board()

    def check_winner(self, player):
        # проверка строк, столбцов и диагоналей
        for row in range(3):
            if all(self.game_board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(self.game_board[row][col] == player for row in range(3)):
                return True
        if all(self.game_board[i][i] == player for i in range(3)) or all(self.game_board[i][2-i] == player for i in range(3)):
            return True
        return False

    # проверка на ничью
    def check_tie(self):
        return all(self.game_board[row][col] is not None for row in range(3) for col in range(3))

    def reset_board(self):
        self.game_board = [[None, None, None], [None, None, None], [None, None, None]]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state=tk.NORMAL)

    # робот пытаеся победить игрока и блокировать его ходы
    def find_best_move(self):
        # Проверка, может ли AI выиграть
        for row in range(3):
            for col in range(3):
                if self.game_board[row][col] is None:
                    self.game_board[row][col] = "O"
                    if self.check_winner("O"):
                        return (row, col)
                    self.game_board[row][col] = None

        # проверка на то что, не выиграет ли игрок на следующем ходу
        for row in range(3):
            for col in range(3):
                if self.game_board[row][col] is None:
                    self.game_board[row][col] = "X"
                    if self.check_winner("X"):
                        self.game_board[row][col] = None
                        return (row, col)
                    self.game_board[row][col] = None

        # если не надо блокировать или победить за один ход, то робот делает любой ход
        best_moves = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]  # приоритетные ходы: углы и центр (чтобы игрок не мог победить)
        if (1, 1) in best_moves:
            row, col = 1, 1
            if self.game_board[row][col] is None:
                return (row, col)
        for move in best_moves:
            row, col = move
            if self.game_board[row][col] is None:
                return (row, col)

        # если не надо блокировать или победить за один ход, то ai делает любой ход
        for row in range(3):
            for col in range(3):
                if self.game_board[row][col] is None:
                    return (row, col)

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()