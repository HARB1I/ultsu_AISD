import numpy as np
import matplotlib.pyplot as plt


# создание матрицы А
def create_matrix(n):
    A = np.random.randint(-10, 11, (n, n))
    return A


# создание подматриц
def split_matrix(A):
    mid = len(A) // 2
    E = A[:mid, :mid]
    B = A[:mid, mid:]
    D = A[mid:, :mid]
    C = A[mid:, mid:]
    return B, C, D, E


# вычисление произведения чисел по периметру матрицы
def calculate_perimeter_product(matrix):
    top = matrix[0, :]
    bottom = matrix[-1, :]
    left = matrix[1:-1, 0]
    right = matrix[1:-1, -1]
    return np.prod(np.concatenate([top, bottom, left, right]))


# Считает сумму элементов в нечетных столбцах, больших K
def calculate_sum_odd_columns(matrix, K):
    odd_columns = matrix[:, 1::2]
    return np.sum(odd_columns[odd_columns > K])


# создание матрицы F
def form_matrix_F(B, C, D, E, K):
    mid = B.shape[0]  # Размер одной подматрицы
    F = np.zeros((B.shape[0] + D.shape[0], B.shape[1] + C.shape[1]), dtype=int)

    sum_in_E = calculate_sum_odd_columns(E, K)
    perimeter_product = calculate_perimeter_product(E)

    if sum_in_E > perimeter_product:
        # симетричная замена C и E
        F[:mid, :mid] = C[::-1, ::-1]
        F[:mid, mid:] = B
        F[mid:, :mid] = D
        F[mid:, mid:] = E[::-1, ::-1]
    else:
        # не симетричная замена C и B
        F[:mid, :mid] = E
        F[:mid, mid:] = C
        F[mid:, :mid] = D
        F[mid:, mid:] = B

    return F


def plot_matrix(matrix):
    plt.imshow(matrix, cmap="viridis")
    plt.colorbar()
    plt.show()


K = int(input("Введите размер K: "))
while True:
    N = int(input("Введите размер матрицы N: "))
    if 6 <= N <= 50 :
        if N % 2 == 1:
            N-=1
            break  # Выход из цикла, если введено корректное значение
    else:
        print(
            "Ошибка: размер матрицы должен быть четным и размер матрицы должен быть не меньше 6 и не больше 50."
        )  # Иначе программа не имеет смысла


A = create_matrix(N)
print(f"Матрица A:\n{A}\n")

B, C, D, E = split_matrix(A)


F = form_matrix_F(B, C, D, E, K)
print(f"Матрица F:\n{F}\n")


det_A = np.linalg.det(A)
sum_diag_F = np.trace(F)

if det_A > sum_diag_F:
    result = np.dot(A, np.linalg.inv(A)) - K * np.linalg.inv(F)
    print(f"Результат выражения A*A^-1 - K*F^-1:\n{result}\n")
else:
    AT = A.T
    G = np.tril(A)
    result = (AT + G - F.T) * K
    print(f"Результат выражения (A^T + G - F^T)*K:\n{result}\n")


plt.figure(figsize=(12, 5))
plt.subplot(1, 3, 1)
plt.title("матрица A")
plt.hist(A.flatten(), bins=range(-10, 12), color="blue")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.title("матрица F")
# plt.hist(F.flatten(), bins=range(-10, 12), alpha=0.7, color='green')
plt.plot(result.flatten(), color="green")
plt.grid(True)

plt.subplot(1, 3, 3)
plt.title("Результирующая матрица")
plt.plot(result.flatten(), "o", color="red")
plt.grid(True)


plt.tight_layout()
plt.show()
