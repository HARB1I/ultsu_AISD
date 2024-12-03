'''
С клавиатуры вводится два числа K и N.
Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10].
Для тестирования использовать не случайное заполнение, а целенаправленное.

Вариант 23
Формируется матрица F следующим образом: если в E сумма чисел, больших К в в нечетных столбцах в области 3 больше,
чем произведение чисел по периметру в области 2, то поменять в Е симметрично области 1 и 2 местами,
иначе С и B поменять местами несимметрично.
При этом матрица А не меняется. После чего вычисляется выражение: (К*А)*F+K*F^T.
Выводятся по мере формирования А, F и все матричные операции последовательно.
Вид матрицы A:
E B
D C

Каждая из матриц B,C,D,E имеет вид:    1
                                     4   2
                                       3
'''

import random


# Функция вывода матриц
def print_matrix(matrix):
    for row in matrix:
        print("|", end='')
        for element in row:
            print("{:3}".format(element), end=' ')
        print("|")


# Транспонирование матрицы
def transpose_matrix(matrix, len_matrix):
    # Создаем новую пустую матрицу для хранения результата
    transposed = [[0 for _ in range(len_matrix)] for _ in range(len_matrix)]
    # Транспонируем матрицу
    for i in range(len_matrix):
        for j in range(len_matrix):
            transposed[j][i] = matrix[i][j]
    return transposed


# ================================ №1 Создание основной матрицы A =========================================
# Вводим значения K и N с клавиатуры
K = int(input("Введите размер K: "))

while True:
    N = int(input("Введите размер матрицы N: "))
    if 6 <= N <= 50:
        break
    else:
        print("Ошибка: Размер матрицы должен быть не меньше 6 и не больше 50.")

# Создаем пустую матрицу A(N, N)
matrix_A = [[0 for _ in range(N)] for _ in range(N)]

# Определяем размер каждой подматрицы
SIZE_submat = N // 2

# Заполняем матрицу A(N, N) случайными числами
for row in range(N):
    for column in range(N):
        matrix_A[row][column] = random.randint(-10, 10)


# Выводим матрицу A
print("Матрица A(N, N):")
print_matrix(matrix_A)


# ================================ №2 Работа с подматрицей Е =========================================
# Создаем и заполняем подматрицу E
matrix_E = [[0 for _ in range(SIZE_submat)] for _ in range(SIZE_submat)]
for row in range(SIZE_submat):
    matrix_E[row] = matrix_A[row][:SIZE_submat]
print("Матрица E:")
print_matrix(matrix_E)


# Подсчет чисел больших К в нечетных столбцах в области 3
count_area_3 = 0
for row in range(SIZE_submat, SIZE_submat // 2, -1):
    for column in range(SIZE_submat - row, row):
        if ((column + 1) % 2 != 0) and matrix_E[row - 1][column] > K:
            count_area_3 += matrix_E[row - 1][column]


# Подсчет произведения чисел по периметру в области 2
mult_area_2 = 1
for row in range(0, SIZE_submat // 2 + SIZE_submat % 2):
    if row != 0:
        mult_area_2 *= matrix_E[row][SIZE_submat - 1] * matrix_E[row][SIZE_submat - 1 - row]
    else:
        mult_area_2 *= matrix_E[row][SIZE_submat - 1] * matrix_E[SIZE_submat - 1 - row][SIZE_submat - 1]
        continue

    if row != SIZE_submat - 1 - row:
        mult_area_2 *= matrix_E[SIZE_submat - 1 - row][SIZE_submat - 1] * \
                        matrix_E[SIZE_submat - 1 - row][SIZE_submat - 1 - row]

# Выводим результаты подсчета
print("Чисел больше К в области 3:", count_area_3)
print("Произведение чисел в области 2:", mult_area_2)


# ================================ №3 Работа с матрицей F =========================================
# Создаем и заполняем матрицу F
matrix_F = [[item for item in row] for row in matrix_A]

# если количество чисел в 3 области больше
if count_area_3 > mult_area_2:
    # меняем в E симметрично области 1 и 2 местами
    for row in range(SIZE_submat//2 + SIZE_submat % 2):
        for column in range(row, SIZE_submat - 1 - row):
            matrix_E[row][column], matrix_E[SIZE_submat - 1 - column][SIZE_submat - 1 - row] = \
                matrix_E[SIZE_submat - 1 - column][SIZE_submat - 1 - row], matrix_E[row][column]

    print("Матрица E после замены местами области 1 и 2 симметрично:")
    print_matrix(matrix_E)

    for row in range(SIZE_submat):
        matrix_F[row][:SIZE_submat] = matrix_E[row]
else:
    # меняем B и C несимметрично
    for row in range(SIZE_submat):
        matrix_F[row][SIZE_submat + N % 2:], matrix_F[row + SIZE_submat + N % 2][SIZE_submat + N % 2:] = \
            matrix_F[row + SIZE_submat + N % 2][SIZE_submat + N % 2:], matrix_F[row][SIZE_submat + N % 2:]

print("Матрица F после всех изменений: ")
print_matrix(matrix_F)


# ================================ №4 Матричные операции =========================================
print("Произведение K*A: ")
mult_KA = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        mult_KA[row][column] = matrix_A[row][column] * K
print_matrix(mult_KA)

print("Суммирование матриц (K * A * F): ")
mult_KAF = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        for k in range(N):
            mult_KAF[row][column] += mult_KA[row][k] * matrix_F[k][column]
print_matrix(mult_KAF)

print("Транспонирование матрицы (F^T): ")
trans_F = transpose_matrix(matrix_F, N)
print_matrix(trans_F)

print("Произведение K * F^T: ")
mult_KFT = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        mult_KFT[row][column] = trans_F[row][column] * K
print_matrix(mult_KFT)


print("итоговый результат (К*А)*F+K*F^T: ")
end_result = [[0 for _ in range(N)] for _ in range(N)]
for row in range(N):
    for column in range(N):
        end_result[row][column] = mult_KAF[row][column] + mult_KFT[row][column]


for row in end_result:
    print("|", end='')
    for element in row:
        print("{:5}".format(element), end=' ')
    print("|")
print("")