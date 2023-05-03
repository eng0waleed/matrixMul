# Python program to find the resultant
# product matrix for a given pair of matrices
# using Divide and Conquer Approach

from multiprocessing import Pool
from itertools import product
import time

p = 4
C_00 = 0
C_01 = 0
C_10 = 0
C_11 = 0
a00 = 0
a01 = 0
a10 = 0
a11 = 0
b00 = 0
b01 = 0
b10 = 0
b11 = 0
# Function to print the matrix


def printMat(a, r, c):
    for i in range(r):
        for j in range(c):
            print(a[i][j], end=" ")
        print()
    print()

# Function to print the matrix


def printt(display, matrix, start_row, start_column, end_row, end_column):
    print(display + " =>\n")
    for i in range(start_row, end_row+1):
        for j in range(start_column, end_column+1):
            print(matrix[i][j], end=" ")
        print()
    print()

# Function to add two matrices
def add_matrix(matrix_A, matrix_B, m):
    matrix_C = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            matrix_C[i][j] = matrix_A[i][j] + matrix_B[i][j]
    return matrix_C

# Function to initialize matrix with zeros


def initWithZeros(a, r, c):
    for i in range(r):
        for j in range(c):
            a[i][j] = 0

# Function to multiply two matrices

def divide_matrices(i, j, m, A, B, a00, a01, a10, a11, b00, b01, b10, b11):
    a00[i][j] = A[i][j]
    a01[i][j] = A[i][j + m]
    a10[i][j] = A[m + i][j]
    a11[i][j] = A[i + m][j + m]
    b00[i][j] = B[i][j]
    b01[i][j] = B[i][j + m]
    b10[i][j] = B[m + i][j]
    b11[i][j] = B[i + m][j + m]

def divide_matrices_wrapper(args):
    i, m, A, B, a00, a01, a10, a11, b00, b01, b10, b11 = args
    for j in range(m):
        divide_matrices(i, j, m, A, B, a00, a01, a10, a11, b00, b01, b10, b11)

def multiply_matrix_parallel(A, B):
    n = len(A[0])
    C = [[0]*n for _ in range(n)]

    if (n == 1):
        C[0][0] = A[0][0] * B[0][0]
        return C

    else:
        m = n // 2

        a00 = [[0] * m for _ in range(m)]
        a01 = [[0] * m for _ in range(m)]
        a10 = [[0] * m for _ in range(m)]
        a11 = [[0] * m for _ in range(m)]
        b00 = [[0] * m for _ in range(m)]
        b01 = [[0] * m for _ in range(m)]
        b10 = [[0] * m for _ in range(m)]
        b11 = [[0] * m for _ in range(m)]

        # for i in range(m):
        #     for j in range(m):
        #         divide_matrices(i, j, m, A, B, a00, a01, a10, a11, b00, b01, b10, b11)


    # # Create the multiprocessing pool
        with Pool(processes=p) as pool:

        #     # Generate the input arguments for each matrix division
            input_args = [(i, m, A, B, a00, a01, a10, a11, b00, b01, b10, b11) for i in range(m) ]
            pool.map(divide_matrices_wrapper, input_args)
        pool.join()
        # pool.closse()

        c1 = add_matrix(multiply_matrix_parallel(a00, b00), multiply_matrix_parallel(a01, b10), m)
        c2 = add_matrix(multiply_matrix_parallel(a00, b01), multiply_matrix_parallel(a01, b11), m)
        c3 = add_matrix(multiply_matrix_parallel(a10, b00), multiply_matrix_parallel(a11, b10), m)
        c4 = add_matrix(multiply_matrix_parallel(a10, b01), multiply_matrix_parallel(a11, b11), m)

        for i in range(m):
            for j in range(m):
                C[i][j] = c1[i][j]
                C[i][j + m] = c2[i][j]
                C[m + i][j] = c3[i][j]
                C[i + m][j + m] = c4[i][j]

        return C


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


# Other functions ...

def writeMatrixToFile(filename_prefix, n_value, matrix, exec_time):
    output_filename = f"{filename_prefix}_{n_value}_output_StraightDivAndConqP.txt"
    info_filename = f"{filename_prefix}_{n_value}_info_StraightDivAndConqP.txt"

    with open(output_filename, 'w') as f:
        n = len(matrix)
        f.write(f"{n}\n")
        for row in matrix:
            f.write(' '.join(str(x) for x in row))
            f.write('\n')

    with open(info_filename, 'a') as f:
        f.write(f"Execution time: {exec_time:.6f} seconds\n")

if __name__ == '__main__':
    readMatrixFromFile('myfile.txt')

    start_time = time.time()
    C = multiply_matrix_parallel(A_matrix, B_matrix)
    exec_time = time.time() - start_time

    print("Result Array =>")
    printMat(C, 4, 4)

    # Write the resultant matrix and execution time to files
    writeMatrixToFile('input1', n_value, C, exec_time)