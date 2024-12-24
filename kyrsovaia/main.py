
import tkinter as tk
import random
import os
import json

BOARD_SIZE = 8
SQUARE_SIZE = 80
selected_square = None
board = None
turn = 'white'
game_over = False
user_data = {}  # Словарь для хранения данных пользователей

def create_board():
    return [['0' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def init_board():
    board = create_board()
    board[6][random.randint(0,BOARD_SIZE - 1)] = 'p1'
    board[1][random.randint(0,BOARD_SIZE - 1)] = 'p2'
    board[7][4] = 'k1'
    board[0][4] = 'k2'
    return board

def get_piece(row, col):
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return board[row][col]
    return None

def set_piece(row, col, piece):
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        board[row][col] = piece

def get_possible_moves(row, col, piece):
    possible_moves = []
    team = 1 if piece.endswith('1') else 2

    if piece == 'p1':
        if row > 0:
            if get_piece(row - 1, col) == '0':
                possible_moves.append((row - 1, col))
                if row == 6 and get_piece(row - 2, col) == '0': 
                    possible_moves.append((row - 2, col))
            if row > 0 and col > 0 and get_piece(row-1, col-1) and get_piece(row-1, col-1).endswith('2'):
              possible_moves.append((row-1, col-1))
            if row > 0 and col < 7 and get_piece(row-1, col+1) and get_piece(row-1, col+1).endswith('2'):
              possible_moves.append((row-1, col+1))
        if row == 0: 
            possible_moves = [(row,col)] 

    elif piece == 'p2':
        if row < BOARD_SIZE - 1:
            if get_piece(row + 1, col) == '0':
                possible_moves.append((row + 1, col))
                if row == 1 and get_piece(row + 2, col) == '0':  
                    possible_moves.append((row + 2, col))
            if row < 7 and col > 0 and get_piece(row+1, col-1) and get_piece(row+1, col-1).endswith('1'):
              possible_moves.append((row+1, col-1))
            if row < 7 and col < 7 and get_piece(row+1, col+1) and get_piece(row+1, col+1).endswith('1'):
              possible_moves.append((row+1, col+1))
        if row == 7: 
            possible_moves = [(row,col)]
    elif piece in ('k1', 'k2'):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    target_piece = get_piece(new_row, new_col)
                    if target_piece == '0' or (target_piece.endswith(str(3-team))):
                        possible_moves.append((new_row, new_col))
    elif piece in ('q1', 'q2'):  
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, BOARD_SIZE): 
                new_row, new_col = row + dr * i, col + dc * i
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    target_piece = get_piece(new_row, new_col)
                    if target_piece == '0':
                        possible_moves.append((new_row, new_col))
                    elif target_piece.endswith(str(3 - team)):
                        possible_moves.append((new_row, new_col))
                        break  
                    else:
                        break  
    return possible_moves

def is_king_captured(team):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if get_piece(r, c) == f'k{team}':
                return False
    return True

def on_click(event):
    global selected_square, turn, game_over
    if game_over:
        return  

    col = event.x // SQUARE_SIZE
    row = event.y // SQUARE_SIZE

    if selected_square:
        old_row, old_col = selected_square
        piece = get_piece(old_row, old_col)
        possible_moves = get_possible_moves(old_row, old_col, piece)

        if (row, col) in possible_moves:
            if piece.startswith('p') and ((row == 0 and piece == 'p1') or (row == 7 and piece == 'p2')): 
                set_piece(row, col, 'q' + piece[-1]) 
            else:
                set_piece(row, col, piece)
            set_piece(old_row, old_col, '0')
            turn = 'black' if turn == 'white' else 'white'
            winner_label.config(text=turn)
            if is_king_captured(1):
                game_over = True
                winner_label.config(text="Черные победили!")
                restart_button.pack()
                resize_and_center(640,690)
            elif is_king_captured(2):
                game_over = True
                winner_label.config(text="Белые победили!")
                restart_button.pack()
                resize_and_center(640,690)
        else:
             selected_square = None 
        selected_square = None

    else:
        piece = get_piece(row, col)
        if piece and ((piece.endswith('1') and turn == 'white') or (piece.endswith('2') and turn == 'black')):
            selected_square = (row, col)

    draw(canvas, board)


def draw(canvas, board):
    canvas.delete("all")
    if game_over == False:
        winner_label.config(text=turn)
    possible_moves = []
    if selected_square:
        row, col = selected_square
        piece = get_piece(row, col)
        possible_moves = get_possible_moves(row, col, piece)

    global piece_images  
    if 'piece_images' not in globals() or piece_images == {}: 
      piece_images = {}
      image_dir = "chess_images/"
      pieces = ['wp', 'wq', 'wk', 'bp', 'bq', 'bk']
      for piece_code in pieces:
          image_path = os.path.join(image_dir, piece_code + ".png")
          try:
              image = tk.PhotoImage(file=image_path)
              piece_images[piece_code] = image
          except tk.TclError:
              print(f"ошибка загрузки картинок '{image_path}': {tk.TclError}")
              piece_images[piece_code] = tk.PhotoImage() 


    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x1 = col * SQUARE_SIZE
            y1 = row * SQUARE_SIZE
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE
            color = "white" if (row + col) % 2 == 0 else "grey"
            if (row, col) in possible_moves:
                color = "lightgreen"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            piece = get_piece(row, col)
            if piece != '0':
                x = x1 + SQUARE_SIZE // 2
                y = y1 + SQUARE_SIZE // 2
                image_key = ""
                if piece.endswith('1'):
                    if piece == 'p1': image_key = "wp"
                    elif piece == 'k1': image_key = "wk"
                    elif piece == 'q1': image_key = "wq"
                else:
                    if piece == 'p2': image_key = "bp"
                    elif piece == 'k2': image_key = "bk"
                    elif piece == 'q2': image_key = "bq"

                if image_key in piece_images:
                    canvas.create_image(x, y, image=piece_images[image_key])


    if selected_square:
        row, col = selected_square
        x1 = col * SQUARE_SIZE
        y1 = row * SQUARE_SIZE
        x2 = x1 + SQUARE_SIZE
        y2 = y1 + SQUARE_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=3)

def restart_game():
    global board, turn, game_over, selected_square
    board = init_board()
    turn = 'white'
    game_over = False
    selected_square = None
    winner_label.config(text="")
    restart_button.pack_forget()
    draw(canvas, board)
    resize_and_center(640,663)

def resize_and_center(window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

def load_user_data():
    """Загружает данные пользователей из файла users.json."""
    global user_data
    try:
        with open("users.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        pass  # Файл еще не существует

def save_user_data():
    """Сохраняет данные пользователей в файл users.json."""
    try:
        with open("users.json", "w") as f:
            json.dump(user_data, f, indent=4)
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")


def register():
    """Регистрирует нового пользователя."""
    username = username_entry.get()
    password = password_entry.get()
    if username in user_data:
        register_label.config(text="Пользователь уже существует!")
    else:
        user_data[username] = {"password": password}
        save_user_data()
        register_label.config(text="Регистрация прошла успешно!")

def login():
    """Авторизует пользователя."""
    username = username_entry.get()
    password = password_entry.get()
    if username in user_data and user_data[username]["password"] == password:
        login_label.config(text="Вход выполнен успешно!")
        login_frame.pack_forget()
        canvas.pack()
        winner_label.pack()
        restart_button.pack()
        start_game()
        


    else:
        login_label.config(text="Неверный логин или пароль!")


def start_game():
    global board, turn, game_over, selected_square
    board = init_board()
    turn = 'white'
    game_over = False
    selected_square = None
    winner_label.config(text="")
    restart_button.pack_forget()
    draw(canvas, board)
    resize_and_center(640,663)
    


root = tk.Tk()
root.resizable(width=False, height=False)
root.title("Chess")

canvas = tk.Canvas(root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)

resize_and_center(BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE + 50)

winner_label = tk.Label(root, text="")
winner_label.pack()

restart_button = tk.Button(root, text="Restart Game", command=restart_game)


# Окно регистрации/авторизации
login_frame = tk.Frame(root)
login_frame.pack()
resize_and_center(250,120)
username_label = tk.Label(login_frame, text="Имя пользователя:")
username_label.grid(row=0, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

password_label = tk.Label(login_frame, text="Пароль:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

register_button = tk.Button(login_frame, text="Зарегистрироваться", command=register)
register_button.grid(row=2, column=0, columnspan=2, sticky="w", pady=15)
register_label = tk.Label(login_frame, text="")
register_label.grid(row=3, column=0, columnspan=2)

login_button = tk.Button(login_frame, text="Войти", command=login)
login_button.grid(row=2, column=1, columnspan=2, sticky="e")
login_label = tk.Label(login_frame, text="")
login_label.grid(row=3, column=1, columnspan=2)

load_user_data()  # Загрузка данных пользователей при запуске

board = init_board()
canvas.bind("<Button-1>", on_click)


root.mainloop()
