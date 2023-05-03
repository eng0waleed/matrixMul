# Python program to find the resultant
# product matrix for a given pair of matrices
# using Divide and Conquer Approach
import multiprocessing as mp
import concurrent.futures

ROW_1 = 4
COL_1 = 4
ROW_2 = 4
COL_2 = 4

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


def add_matrix(matrix_A, matrix_B, matrix_C, m):
    for i in range(m):
        for j in range(m):
            matrix_C[i][j] = matrix_A[i][j] + matrix_B[i][j]

# Function to initialize matrix with zeros


def initWithZeros(a, r, c):
    for i in range(r):
        for j in range(c):
            a[i][j] = 0

def multiply_matrices(args):
    return multiply_matrix(*args)

# Function to multiply two matrices
def multiply_matrix(A, B, threshold=64):
    n = len(A[0])
    C = [[0] * n for _ in range(n)]

    if n <= threshold:
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
    elif n == 1:
        C[0][0] = A[0][0] * B[0][0]
    else:
        m = n // 2

        # Split the matrices into 4 submatrices
        a00 = [[A[i][j] for j in range(m)] for i in range(m)]
        a01 = [[A[i][j] for j in range(m, n)] for i in range(m)]
        a10 = [[A[i][j] for j in range(m)] for i in range(m, n)]
        a11 = [[A[i][j] for j in range(m, n)] for i in range(m, n)]

        b00 = [[B[i][j] for j in range(m)] for i in range(m)]
        b01 = [[B[i][j] for j in range(m, n)] for i in range(m)]
        b10 = [[B[i][j] for j in range(m)] for i in range(m, n)]
        b11 = [[B[i][j] for j in range(m, n)] for i in range(m, n)]

        # Create a process pool and submit matrix multiplication tasks
        with concurrent.futures.ProcessPoolExecutor() as executor:
            c1, c2, c3, c4, c5, c6, c7, c8 = executor.map(multiply_matrices, [
                (a00, b00), (a01, b10), (a00, b01), (a01, b11),
                (a10, b00), (a11, b10), (a10, b01), (a11, b11)
            ])

        # Combine the results
        for i in range(m):
            for j in range(m):
                C[i][j] = c1[i][j] + c2[i][j]
                C[i][j + m] = c3[i][j] + c4[i][j]
                C[m + i][j] = c5[i][j] + c6[i][j]
                C[m + i][j + m] = c7[i][j] + c8[i][j]

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
        n = len(matrix)
        f.write(f"{n}\n")
        for row in matrix:
            f.write(" ".join(str(x) for x in row) + "\n")

def main():
    readMatrixFromFile('myfile.txt')
    C = multiply_matrix(A_matrix, B_matrix)

    writeMatrixToFile('output.txt', C)

if __name__ == '__main__':
    main()