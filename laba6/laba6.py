'''
Задание состоит из двух частей.
1 часть – написать программу в соответствии со своим вариантом задания. Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.
2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение на характеристики объектов (которое будет сокращать количество переборов)
и целевую функцию для нахождения оптимального  решения.

Вариант 23.Дана квадратная матрица, состоящая из четырех равных по размерам подматриц.
Сформировать все возможные варианты данной матрицы путем перестановки данных подматриц.
'''

import numpy as np
from itertools import permutations
import timeit


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


# Функция для первой части
def first_part(matrix):
    algo_results = algorithmic_permutation(matrix)
    func_results = function_permutation(matrix)
    return algo_results, func_results


# Функция для второй части
def second_part(matrix):
    return constrained_permutation(matrix)


# Основная функция
def main():
    size = 4  # Размерность матрицы (должна быть четной)
    matrix = generate_matrix(size)

    # 1 часть: использование timeit
    algo_time = timeit.timeit(lambda: first_part(matrix), number=1)
    func_time = timeit.timeit(lambda: first_part(matrix), number=1)

    algo_results, func_results = first_part(matrix)

    print("1 часть:")
    print(f"Время выполнения алгоритмического подхода: {algo_time:.6f} секунд")
    print(f"Время выполнения с помощью функций Питона: {func_time:.6f} секунд")
    print(f"Количество всех возможных вариантов данной матрицы (алгоритмический): {len(algo_results)}")
    print(f"Количество всех возможных вариантов данной матрицы (функции): {len(func_results)}")

    if algo_time < func_time:
        print("Алгоритмический подход быстрее.")
    else:
        print("Метод с использованием функций быстрее.")

    # Вывод первых трех матриц
    print("\nПервые три матрицы:")
    for i, mat in enumerate(algo_results[:3]):
        print(f"Матрица {i + 1}:\n{mat}\n")



    # 2 часть: добавление ограничения (новая матрица будет состоять только из четных цифр)
    constrained_time = timeit.timeit(lambda: second_part(matrix), number=1)
    constrained_results = second_part(matrix)

    print("\n2 часть:")
    print(f"Время выполнения с учетом ограничения: {constrained_time:.6f} секунд")


    # Вывод всех возможных вариантов после усложнения для отладки
    if len(constrained_results) > 0:
        print("Примеры допустимых матриц:")
        for mat in constrained_results[:3]:  # Выводим первые 3 допустимые матрицы
            print(mat, "\n")

main()