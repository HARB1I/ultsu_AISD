import numpy as np
from itertools import permutations
import timeit
import tkinter as tk
from tkinter import scrolledtext, messagebox


# Генерация квадратной матрицы 2x2 из подматриц
def generate_matrix(size):
    return np.arange(1, size * size + 1).reshape(size, size)


# Алгоритмический способ (без использования функций)
def algorithmic_permutation(matrix):
    size = matrix.shape[0]
    submatrices = [matrix[0:size // 2, 0:size // 2],
                   matrix[0:size // 2, size // 2:size],
                   matrix[size // 2:size, 0:size // 2],
                   matrix[size // 2:size, size // 2:size]
                   ]

    all_permutations = []
    for perm in permutations(submatrices):
        new_matrix = np.block([[perm[0], perm[1]],
                               [perm[2], perm[3]]])
        all_permutations.append(new_matrix)
    return all_permutations


# Использование функций Питона
def function_permutation(matrix):
    size = matrix.shape[0]
    submatrices = [matrix[0:size // 2, 0:size // 2],
                   matrix[0:size // 2, size // 2:size],
                   matrix[size // 2:size, 0:size // 2],
                   matrix[size // 2:size, size // 2:size]
                   ]

    return [np.block([[perm[0], perm[1]],
                      [perm[2], perm[3]]]) for perm in permutations(submatrices)]


# Ограничение: матрица должна состоять только из четных чисел
def constrained_permutation(matrix):
    size = matrix.shape[0]
    # Создаем четную матрицу
    even_matrix = np.arange(2, size * size * 2 + 2, 2).reshape(size, size)
    submatrices = [even_matrix[0:size // 2, 0:size // 2],
                   even_matrix[0:size // 2, size // 2:size],
                   even_matrix[size // 2:size, 0:size // 2],
                   even_matrix[size // 2:size, size // 2:size]
                   ]

    valid_permutations = []
    for perm in permutations(submatrices):
        new_matrix = np.block([[perm[0], perm[1]],
                               [perm[2], perm[3]]])
        # Проверяем, чтобы каждая подматрица состояла только из четных чисел
        if all(np.all(submatrix % 2 == 0) for submatrix in perm):
            valid_permutations.append(new_matrix)  # Добавляем подходящие матрицы
    return valid_permutations


# Функция для второй части
def second_part(size):
    matrix = generate_matrix(size)
    return constrained_permutation(matrix)


# GUI
def run_second_part():
    try:
        size = int(entry_size.get())
        if size % 2 != 0 or size <= 0:
            raise ValueError("Размерность должна быть положительным четным числом.")

        start_time = timeit.default_timer()
        results = second_part(size)
        elapsed_time = timeit.default_timer() - start_time

        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Время выполнения с учетом ограничения: {elapsed_time:.6f} секунд\n")

        if results:
            output_text.insert(tk.END, "Примеры допустимых матриц (первые три):\n")
            for i, mat in enumerate(results[:3]):
                output_text.insert(tk.END, f"Матрица {i + 1}:\n{mat}\n")
        else:
            output_text.insert(tk.END, "Нет допустимых матриц.\n")

    except ValueError as e:
        messagebox.showerror("Ошибка ввода", str(e))



root = tk.Tk()
root.title("Перестановка подматриц")


window_width = 460
window_height = 400
root.geometry(f"{window_width}x{window_height}")


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


tk.Label(root, text="Введите размерность матрицы (четное число):").pack()
entry_size = tk.Entry(root)
entry_size.pack()


btn_run = tk.Button(root, text="Запустить расчет", command=run_second_part)
btn_run.pack()


output_text = scrolledtext.ScrolledText(root, width=75, height=20)
output_text.pack()


root.mainloop()
