# Python program to find the resultant
# product matrix for a given pair of matrices
# using Divide and Conquer Approach
import multiprocessing as mp
import concurrent.futures
import time
import threading
# from concurrent.futures import ProcessPoolExecutor

# Function to print the matrix

A_matrix = []
B_matrix = []
A_matrix_temp = []
B_matrix_temp = []

def reset_matrices():
    global A_matrix
    global B_matrix
    A_matrix = A_matrix_temp
    B_matrix = B_matrix_temp


def add_matrix(matrix_A, matrix_B, matrix_C, m):
    for i in range(m):
        for j in range(m):
            matrix_C[i][j] = matrix_A[i][j] + matrix_B[i][j]

def initWithZeros(a, r, c):
    for i in range(r):
        for j in range(c):
            a[i][j] = 0

def multiply_matrices(args):
    return multiply_matrix(*args)

def split_matrix(args):
    A, start_row, end_row, start_col, end_col = args
    return [[A[i][j] for j in range(start_col, end_col)] for i in range(start_row, end_row)]

def combine_results(C, submatrix1, submatrix2, start_row, start_col):
    for i in range(len(submatrix1)):
        for j in range(len(submatrix1[0])):
            C[start_row + i][start_col + j] = submatrix1[i][j] + submatrix2[i][j]

def multiply_matrix(A, B, num_processes=8, threshold=64):
    n = len(A[0])
    C = [[0] * n for _ in range(n)]

    if n <= threshold:
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        # C = multiply_matrix_seq(A,B)
    # elif n == 1:
    #     C[0][0] = A[0][0] * B[0][0]
    else:
        m = n // 2

        # Split the matrices into 4 submatrices
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
            a00, a01, a10, a11 = executor.map(split_matrix, [
                (A, 0, m, 0, m),
                (A, 0, m, m, n),
                (A, m, n, 0, m),
                (A, m, n, m, n)
            ])

            b00, b01, b10, b11 = executor.map(split_matrix, [
                (B, 0, m, 0, m),
                (B, 0, m, m, n),
                (B, m, n, 0, m),
                (B, m, n, m, n)
            ])

        inputs = [
            (a00, b00), (a01, b10), (a00, b01), (a01, b11),
            (a10, b00), (a11, b10), (a10, b01), (a11, b11)
        ]

        with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
            results = list(executor.map(multiply_matrix, inputs))
            # concurrent.futures.wait(results)
            
        # Combine the results
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
            combine_futures = [
                executor.submit(combine_results, (C, results[0], results[1], 0, 0)),
                executor.submit(combine_results, (C, results[2], results[3], 0, m)),
                executor.submit(combine_results, (C, results[4], results[5], m, 0)),
                executor.submit(combine_results, (C, results[6], results[7], m, m))
            ]
            for future in combine_futures:
                future.result()
            
    return C

def readMatrixFromFile(filename):
    global A_matrix
    global B_matrix
    with open(filename) as f:
        n = int(f.readline())
        print(n)
        for i in range(n):
            A_matrix.append([int(x) for x in f.readline().split()])
        for i in range(n):
            B_matrix.append([int(x) for x in f.readline().split()])

def writeMatrixToFile(filename, matrix):
    with open(filename, 'w') as f:
        n = len(matrix)
        f.write(f"{n}\n")
        for row in matrix:
            f.write(" ".join(str(x) for x in row) + "\n")


def multiply_matrix_seq(A, B, threshold=64):
    n = len(A[0])
    C = [[0]*n for _ in range(n)]

    # if (n == 1):
    #     C[0][0] = A[0][0] * B[0][0]
    if n <= threshold:
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]

    else:
        m = n // 2

        C_00 = [[0]*m for _ in range(m)]
        C_01 = [[0]*m for _ in range(m)]
        C_10 = [[0]*m for _ in range(m)]
        C_11 = [[0]*m for _ in range(m)]
        a00 = [[0]*m for _ in range(m)]
        a01 = [[0]*m for _ in range(m)]
        a10 = [[0]*m for _ in range(m)]
        a11 = [[0]*m for _ in range(m)]
        b00 = [[0]*m for _ in range(m)]
        b01 = [[0]*m for _ in range(m)]
        b10 = [[0]*m for _ in range(m)]
        b11 = [[0]*m for _ in range(m)]

        for i in range(m):
            for j in range(m):
                a00[i][j] = A[i][j]
                a01[i][j] = A[i][j + m]
                a10[i][j] = A[m + i][j]
                a11[i][j] = A[i + m][j + m]
                b00[i][j] = B[i][j]
                b01[i][j] = B[i][j + m]
                b10[i][j] = B[m + i][j]
                b11[i][j] = B[i + m][j + m]

        c1 = multiply_matrix_seq(a00, b00)
        c2 = multiply_matrix_seq(a01, b10)
        c3 = multiply_matrix_seq(a00, b01)
        c4 = multiply_matrix_seq(a01, b11)
        c5 = multiply_matrix_seq(a10, b00)
        c6 = multiply_matrix_seq(a11, b10)
        c7 = multiply_matrix_seq(a10, b01)
        c8 = multiply_matrix_seq(a11, b11)

        for i in range(m):
            for j in range(m):
                C_00[i][j] = c1[i][j] + c2[i][j]
                C_01[i][j] = c3[i][j] + c4[i][j]
                C_10[i][j] = c5[i][j] + c6[i][j]
                C_11[i][j] = c7[i][j] + c8[i][j]
                C[i][j] = C_00[i][j]
                C[i][j + m] = C_01[i][j]
                C[m + i][j] = C_10[i][j]
                C[i + m][j + m] = C_11[i][j]

    return C


def partition_matrix(M, size, n):
    a = [[M[i][j] for j in range(size)] for i in range(size)]
    b = [[M[i][j] for j in range(size, n)] for i in range(size)]
    c = [[M[i][j] for j in range(size)] for i in range(size, n)]
    d = [[M[i][j] for j in range(size, n)] for i in range(size, n)]
    return a, b, c, d


def add_matrices(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C


def subtract_matrices(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def combine_matrices(C, a11, a12, a21, a22):
    n = len(a11)
    for i in range(n):
        for j in range(n):
            C[i][j] = a11[i][j]
            C[i][j + n] = a12[i][j]
            C[i + n][j] = a21[i][j]
            C[i + n][j + n] = a22[i][j]


def strassen_sequential(A, B, threshold=64):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    if n <= threshold:
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
    else:
        newSize = n // 2

        a11, a12, a21, a22 = partition_matrix(A, newSize, n)
        b11, b12, b21, b22 = partition_matrix(B, newSize, n)

        m1 = strassen_sequential(add_matrices(a11, a22), add_matrices(b11, b22))
        m2 = strassen_sequential(add_matrices(a21, a22), b11)
        m3 = strassen_sequential(a11, subtract_matrices(b12, b22))
        m4 = strassen_sequential(a22, subtract_matrices(b21, b11))
        m5 = strassen_sequential(add_matrices(a11, a12), b22)
        m6 = strassen_sequential(subtract_matrices(a21, a11), add_matrices(b11, b12))
        m7 = strassen_sequential(subtract_matrices(a12, a22), add_matrices(b21, b22))

        c11 = add_matrices(subtract_matrices(add_matrices(m1, m4), m5), m7)
        c12 = add_matrices(m3, m5)
        c21 = add_matrices(m2, m4)
        c22 = add_matrices(subtract_matrices(add_matrices(m1, m3), m2), m6)

        combine_matrices(C, c11, c12, c21, c22)
    return C

def strassen_parallel(A, B, num_processes=8, threshold=64):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    if n <= threshold:
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]

    elif n == 1:
        C[0][0] = A[0][0] * B[0][0]
    else:
        new_size = n // 2

        a11, a12, a21, a22 = partition_matrix(A, new_size, n)
        b11, b12, b21, b22 = partition_matrix(B, new_size, n)

        
        add_a11_a22 = add_matrices(a11, a22)
        add_b11_b22 = add_matrices(b11, b22)
        add_a21_a22 = add_matrices(a21, a22)
        sub_b12_b22 = subtract_matrices(b12, b22)
        sub_a21_a11 = subtract_matrices(a21, a11)
        sub_b21_b11 = subtract_matrices(b21, b11)
        sub_a12_a22 = subtract_matrices(a12, a22)
        add_a11_a12 = add_matrices(a11, a12)
        add_b11_b12 = add_matrices(b11, b12)
        add_b21_b22 = add_matrices(b21, b22)

        with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = [
                executor.submit(strassen_parallel, add_a11_a22, add_b11_b22),
                executor.submit(strassen_parallel, add_a21_a22, b11),
                executor.submit(strassen_parallel, a11, sub_b12_b22),
                executor.submit(strassen_parallel, a22, sub_b21_b11),
                executor.submit(strassen_parallel, add_a11_a12, b22),
                executor.submit(strassen_parallel, sub_a21_a11, add_b11_b12),
                executor.submit(strassen_parallel, sub_a12_a22, add_b21_b22)
            ]

            m1, m2, m3, m4, m5, m6, m7 = [
                future.result() for future in futures]

        c11 = add_matrices(subtract_matrices(add_matrices(m1, m4), m5), m7)
        c12 = add_matrices(m3, m5)
        c21 = add_matrices(m2, m4)
        c22 = add_matrices(subtract_matrices(add_matrices(m1, m3), m2), m6)

        combine_matrices(C, c11, c12, c21, c22)

    return C

def main():
    index = int(input("enter power value for multiply: "))
    input_filename = 'test_power_'+str(index)+'_matrices.txt'
    readMatrixFromFile(input_filename)

    methods = [
        ('StraightDivAndConqP', multiply_matrix),
        ('StraightDivAndConqSeq', multiply_matrix_seq),
        ('StrassenSeq', strassen_sequential),
        ('StrassenParallel', strassen_parallel),
        # Add other multiplication methods here
    ]

    for method_name, method in methods:
        start_time = time.time()
        C = method(A_matrix, B_matrix)
        elapsed_time = time.time() - start_time

        output_file = f"{input_filename}_{index}_output_{method_name}.txt"
        writeMatrixToFile(output_file, C)

        info_file = f"{input_filename}_{index}_info_{method_name}.txt"
        with open(info_file, 'w') as f:
            f.write(f"{elapsed_time:.2f} seconds\n")
            
        all_info = f"{index}_info.txt"
        with open(all_info, 'a') as f:
            f.write(f' {time.strftime(" %Y-%m-%d %H: %M: %S", time.localtime(time.time()))} | {method_name}\t:    {elapsed_time: .2f} seconds\n')





if __name__ == '__main__':
    main()
