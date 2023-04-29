# Purpose: Multiply two matrices using straightforward sequential algorithm

# This is the straightforward sequential algorithm for multiplying two matrices.
# It is a straightforward implementation of the algorithm, with no optimizations.
# It is intended to be used as a baseline for comparison with other algorithms.

# The algorithm is as follows:
# 1. Read the two matrices from a file.
# 2. Multiply the two matrices.
# 3. Write the result to a file.

# The matrices are stored in the file as follows:
# 1. The first line contains the dimension of the matrices.
# 2. The next n lines contain the elements of the first matrix.
# 3. The next n lines contain the elements of the second matrix.

from multiprocessing import Pool

def StraightDivAndConq(A, B):
    n = len(A)
    C = [[0]*n]*n
    print(C)

    for i in range(n):
        for j in range(n):
            C[i][j] = 0
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def StraightDivAndConqP(A, B):
    n = len(A)
    C = [[0]*n]*n
    print(C)
    pool = Pool(processes=n)
    C = pool.map(multiply_straightforward, [(A, B, i, n) for i in range(n)])
    return C

def multiply_straightforward(args):
    A, B, i, n = args
    return [sum([A[i][k] * B[k][j] for k in range(n)]) for j in range(n)]

# def straightforward_divide_and_conquer_matrix_multiplication( A, B, C, n):
#     # C = [[0]*n]*n
#     if (n == 1):
#         C[0][0] = A[0][0] * B[0][0]
#         return
    

#     m = n / 2
#     m = int(m)
#     A11 = [[0]*m]*m
#     A12 = [[0]*m]*m
#     A21 = [[0]*m]*m
#     A22 = [[0]*m]*m
#     B11 = [[0]*m]*m
#     B12 = [[0]*m]*m
#     B21 = [[0]*m]*m
#     B22 = [[0]*m]*m
#     C11 = [[0]*m]*m
#     C12 = [[0]*m]*m
#     C21 = [[0]*m]*m
#     C22 = [[0]*m]*m
#     # Divide matrices A, B, and C into 4 submatrices of size m x m

#     for i in range (m) :
#         for j in range (m) :
#             A11[i][j] = A[i][j]
#             A12[i][j] = A[i][j + m]
#             A21[i][j] = A[i + m][j]
#             A22[i][j] = A[i + m][j + m]
#             B11[i][j] = B[i][j]
#             B12[i][j] = B[i][j + m]
#             B21[i][j] = B[i + m][j]
#             B22[i][j] = B[i + m][j + m]
#             C11[i][j] = 0
#             C12[i][j] = 0
#             C21[i][j] = 0
#             C22[i][j] = 0

#     straightforward_divide_and_conquer_matrix_multiplication(A11, B11, C11, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A12, B21, C11, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A11, B12, C12, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A12, B22, C12, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A21, B11, C21, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A22, B21, C21, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A21, B12, C22, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A22, B22, C22, m)
#     # Combine the submatrices into the result matrix C
#     for i in range (m) :
#         for j in range (m) :
#             C[i][j] = C11[i][j] + C12[i][j]
#             C[i][j + m] = C11[i][j + m] + C12[i][j + m]
#             C[i + m][j] = C21[i][j] + C22[i][j]
#             C[i + m][j + m] = C21[i][j + m] + C22[i][j + m]

#     return C


# def straightforward_divide_and_conquer_matrix_multiplication(A, B, C, n):
#     if n == 1:
#         C[0][0] = A[0][0] * B[0][0]
#         return

#     m = n // 2
#     A11, A12, A21, A22 = A[:m, :m], A[:m, m:], A[m:, :m], A[m:, m:]
#     B11, B12, B21, B22 = B[:m, :m], B[:m, m:], B[m:, :m], B[m:, m:]
#     C11, C12, C21, C22 = C[:m, :m], C[:m, m:], C[m:, :m], C[m:, m:]

#     straightforward_divide_and_conquer_matrix_multiplication(A11, B11, C11, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A12, B21, C11, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A11, B12, C12, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A12, B22, C12, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A21, B11, C21, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A22, B21, C21, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A21, B12, C22, m)
#     straightforward_divide_and_conquer_matrix_multiplication(A22, B22, C22, m)

#     C[:m, :m] = C11
#     C[:m, m:] = C12
#     C[m:, :m] = C21
#     C[m:, m:] = C22

# write a divide and conquer matrix multiplication algorithm
# that takes two n x n matrices A and B and returns their product C = A * B
# def divide_and_conquer_matrix_multiplication(A, B, C, n):
#     if n == 1:
#         C[0][0] = A[0][0] * B[0][0]
#         return

#     m = n // 2
#     A11, A12, A21, A22 = A[:m, :m], A[:m, m:], A[m:, :m], A[m:, m:]
#     B11, B12, B21, B22 = B[:m, :m], B[:m, m:], B[m:, :m], B[m:, m:]
#     C11, C12, C21, C22 = C[:m, :m], C[:m, m:], C[m:, :m], C[m:, m:]

#     divide_and_conquer_matrix_multiplication(A11, B11, C11, m)
#     divide_and_conquer_matrix_multiplication(A12, B21, C11, m)
#     divide_and_conquer_matrix_multiplication(A11, B12, C12, m)
#     divide_and_conquer_matrix_multiplication(A12, B22, C12, m)
#     divide_and_conquer_matrix_multiplication(A21, B11, C21, m)
#     divide_and_conquer_matrix_multiplication(A22, B21, C21, m)
#     divide_and_conquer_matrix_multiplication(A21, B12, C22, m)



A_matrix = []
B_matrix = []

def readMatrixFromFile(filename):
    global A_matrix
    global B_matrix
    with open(filename) as f:
        n = int(f.readline())
        setMatrixDimentions(n)
        for i in range(n):
            A_matrix.append([int(x) for x in f.readline().split()])
        for i in range(n):
            B_matrix.append([int(x) for x in f.readline().split()])

n_value = 0

def setMatrixDimentions(n):
    global n_value
    n_value = n

def writeMatrixToFile(filename, matrix):
    with open(filename, 'w') as f:
        f.write(str(n_value) + '\n')
        for i in range(n_value):
            for j in range(n_value):
                f.write(str(matrix[i][j]) + ' ')
            f.write('\n')

if __name__ == '__main__':
    readMatrixFromFile('myfile.txt')
    # C_matrix = StraightDivAndConq(A_matrix, B_matrix)
    C = [[0]*n_value]*n_value

    C_matrix = straightforward_divide_and_conquer_matrix_multiplication(A_matrix, B_matrix, C, n_value)
    writeMatrixToFile('myfile.out', C_matrix)