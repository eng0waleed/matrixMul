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


def multiply_matrix(A, B):
    n = len(A)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
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

def writeMatrixToFile(filename, matrix):
    with open(filename, 'w') as f:
        f.write(str(n_value) + '\n')
        for i in range(n_value):
            for j in range(n_value):
                f.write(str(matrix[i][j]) + ' ')
            f.write('\n')

if __name__ == '__main__':
    readMatrixFromFile('myfile.txt')
    C_matrix = multiply_matrix(A_matrix, B_matrix)
    writeMatrixToFile('myfile.out', C_matrix)