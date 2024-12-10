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


# Генерация квадратной матрицы
def generate_matrix(size):
    return np.arange(1, size * size + 1).reshape(size, size)


# Алгоритмический способ (без использования функций)
def algorithmic_permutation(matrix):
    size = matrix.shape[0]
    submatrices = [matrix[0:size // 2, 0:size // 2],
                   matrix[0:size // 2, size // 2:size],
                   matrix[size // 2:size, 0:size // 2],
                   matrix[size // 2:size, size // 2:size]]

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
                   matrix[size // 2:size, size // 2:size]]

    return [np.block([[perm[0], perm[1]],
                      [perm[2], perm[3]]]) for perm in permutations(submatrices)]


# Ограничение: матрица должна содержать числа от 1 до 5
def constrained_permutation(matrix):
    size = matrix.shape[0]

    # Генерация уникальных чисел от 1 до 5 для каждой подматрицы
    unique_numbers = np.array([1, 2, 3, 4, 5])

    # Создание подматрицы с уникальными числами
    submatrices = [
        np.random.choice(unique_numbers, (size // 2, size // 2), replace=False),
        np.random.choice(unique_numbers, (size // 2, size // 2), replace=False),
        np.random.choice(unique_numbers, (size // 2, size // 2), replace=False),
        np.random.choice(unique_numbers, (size // 2, size // 2), replace=False)
    ]

    valid_permutations = []
    for perm in permutations(submatrices):
        new_matrix = np.block([[perm[0], perm[1]],
                               [perm[2], perm[3]]])
        # Проверка, чтобы каждая подматрица состояла только из уникальных чисел
        if len(set(new_matrix.flatten())) <= size * size:  # Все элементы должны быть уникальны
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


def main():
    size = 4  # Размерность матрицы (должна быть четной)
    matrix = generate_matrix(size)

    # 1 часть: использование timeit
    algo_time = timeit.timeit(lambda: first_part(matrix), number=1)
    func_time = timeit.timeit(lambda: function_permutation(matrix), number=1)

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

    # Вторая часть: применение ограничения на уникальные числа
    constrained_results = second_part(matrix)
    print(f"Количество вариантов с учетом ограничения на уникальные числа: {len(constrained_results)}")

main()