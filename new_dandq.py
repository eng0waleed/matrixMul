# Python program to find the resultant
# product matrix for a given pair of matrices
# using Divide and Conquer Approach

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


def add_matrix(matrix_A, matrix_B, matrix_C, split_index):
    for i in range(split_index):
        for j in range(split_index):
            matrix_C[i][j] = matrix_A[i][j] + matrix_B[i][j]

# Function to initialize matrix with zeros


def initWithZeros(a, r, c):
    for i in range(r):
        for j in range(c):
            a[i][j] = 0

# Function to multiply two matrices


def multiply_matrix(matrix_A, matrix_B):
    col_1 = len(matrix_A[0])
    row_1 = len(matrix_A)
    col_2 = len(matrix_B[0])

    C = [[0 for x in range(col_2)] for y in range(row_1)]

    if (col_1 == 1):
        C[0][0] = matrix_A[0][0] * matrix_B[0][0]

    else:
        split_index = col_1 // 2

        row_vector = [0] * split_index
        
        

        C_00 = [
            [0 for x in range(split_index)] for y in range(split_index)]
        C_01 = [
            [0 for x in range(split_index)] for y in range(split_index)]
        C_10 = [
            [0 for x in range(split_index)] for y in range(split_index)]
        C_11 = [
            [0 for x in range(split_index)] for y in range(split_index)]
        a00 = [[0 for x in range(split_index)] for y in range(split_index)]
        a01 = [[0 for x in range(split_index)] for y in range(split_index)]
        a10 = [[0 for x in range(split_index)] for y in range(split_index)]
        a11 = [[0 for x in range(split_index)] for y in range(split_index)]
        b00 = [[0 for x in range(split_index)] for y in range(split_index)]
        b01 = [[0 for x in range(split_index)] for y in range(split_index)]
        b10 = [[0 for x in range(split_index)] for y in range(split_index)]
        b11 = [[0 for x in range(split_index)] for y in range(split_index)]

        for i in range(split_index):
            for j in range(split_index):
                a00[i][j] = matrix_A[i][j]
                a01[i][j] = matrix_A[i][j + split_index]
                a10[i][j] = matrix_A[split_index + i][j]
                a11[i][j] = matrix_A[i + split_index][j + split_index]
                b00[i][j] = matrix_B[i][j]
                b01[i][j] = matrix_B[i][j + split_index]
                b10[i][j] = matrix_B[split_index + i][j]
                b11[i][j] = matrix_B[i + split_index][j + split_index]

        c1 = multiply_matrix(a00, b00)
        c2 = multiply_matrix(a01, b10)
        c3 = multiply_matrix(a00, b01)
        c4 = multiply_matrix(a01, b11)
        c5 = multiply_matrix(a10, b00)
        c6 = multiply_matrix(a11, b10)
        c7 = multiply_matrix(a10, b01)
        c8 = multiply_matrix(a11, b11)

        for i in range(split_index):
            for j in range(split_index):
                C_00[i][j] = c1[i][j] + c2[i][j]
                C_01[i][j] = c3[i][j] + c4[i][j]
                C_10[i][j] = c5[i][j] + c6[i][j]
                C_11[i][j] = c7[i][j] + c8[i][j]

        for i in range(split_index):
            for j in range(split_index):
                C[i][j] = C_00[i][j]
                C[i][j + split_index] = C_01[i][j]
                C[split_index + i][j] = C_10[i][j]
                C[i + split_index][j + split_index] = C_11[i][j]

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


readMatrixFromFile('myfile.txt')
C = multiply_matrix(A_matrix, B_matrix)

print("Result Array =>")
printMat(C, 4, 4)
