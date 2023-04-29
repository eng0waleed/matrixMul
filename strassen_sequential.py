def straightforward_divide_and_conquer_matrix_multiplication( A, B, n):
    
    if (n == 1):
        C[0][0] = A[0][0] * B[0][0]
        return
    

    m = n / 2
    A11, A12, A21, A22 = [[0]*m]*m
    B11, B12, B21, B22 = [[0]*m]*m
    C11, C12, C21, C22 = [[0]*m]*m
    # Divide matrices A, B, and C into 4 submatrices of size m x m

    for i in range (0,m) :
        for j in range (0,m) :
            A11[i][j] = A[i][j]
            A12[i][j] = A[i][j + m]
            A21[i][j] = A[i + m][j]
            A22[i][j] = A[i + m][j + m]
            B11[i][j] = B[i][j]
            B12[i][j] = B[i][j + m]
            B21[i][j] = B[i + m][j]
            B22[i][j] = B[i + m][j + m]
            C11[i][j] = 0
            C12[i][j] = 0
            C21[i][j] = 0
            C22[i][j] = 0

    straightforward_divide_and_conquer_matrix_multiplication(A11, B11, C11, m)
    straightforward_divide_and_conquer_matrix_multiplication(A12, B21, C11, m)
    straightforward_divide_and_conquer_matrix_multiplication(A11, B12, C12, m)
    straightforward_divide_and_conquer_matrix_multiplication(A12, B22, C12, m)
    straightforward_divide_and_conquer_matrix_multiplication(A21, B11, C21, m)
    straightforward_divide_and_conquer_matrix_multiplication(A22, B21, C21, m)
    straightforward_divide_and_conquer_matrix_multiplication(A21, B12, C22, m)
    straightforward_divide_and_conquer_matrix_multiplication(A22, B22, C22, m)
    # Combine the submatrices into the result matrix C
    for i in range (0,m) :
        for j in range (0,m) :
            C[i][j] = C11[i][j] + C12[i][j]
            C[i][j + m] = C11[i][j + m] + C12[i][j + m]
            C[i + m][j] = C21[i][j] + C22[i][j]
            C[i + m][j + m] = C21[i][j + m] + C22[i][j + m]

    return C