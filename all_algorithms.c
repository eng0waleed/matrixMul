#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>
#include <string.h>

#define ROW_1 4
#define COL_1 4
#define ROW_2 4
#define COL_2 4
#define THRESHOLD 64

typedef struct
{
    int **matrix;
    int start_row;
    int end_row;
    int start_col;
    int end_col;
} SubMatrix;

typedef struct
{
    int **matrix;
    int n;
} Matrix;

void initWithZeros(int **a, int r, int c)
{
    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            a[i][j] = 0;
        }
    }
}

SubMatrix *split_matrix(int **A, int start_row, int end_row, int start_col, int end_col)
{
    SubMatrix *submatrix = (SubMatrix *)malloc(sizeof(SubMatrix));
    int rows = end_row - start_row;
    int cols = end_col - start_col;
    int **matrix = (int **)malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++)
    {
        matrix[i] = (int *)malloc(cols * sizeof(int));
        for (int j = 0; j < cols; j++)
        {
            matrix[i][j] = A[i + start_row][j + start_col];
        }
    }
    submatrix->matrix = matrix;
    submatrix->start_row = start_row;
    submatrix->end_row = end_row;
    submatrix->start_col = start_col;
    submatrix->end_col = end_col;
    return submatrix;
}

void combine_results(int **C, int **submatrix1, int **submatrix2, int start_row, int start_col)
{
    int rows = sizeof(submatrix1) / sizeof(submatrix1[0]);
    int cols = sizeof(submatrix1[0]) / sizeof(int);
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            C[start_row + i][start_col + j] = submatrix1[i][j] + submatrix2[i][j];
        }
    }
}

int **multiply_matrix(int **A, int **B, int n, int num_processes)
{
    int **C = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
    {
        C[i] = (int *)malloc(n * sizeof(int));
    }
    initWithZeros(C, n, n);

    if (n <= THRESHOLD)
    {
#pragma omp parallel for num_threads(num_processes)
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                for (int k = 0; k < n; k++)
                {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }
    else if (n == 1)
    {
        C[0][0] = A[0][0] * B[0][0];
    }
    else
    {
        int m = n / 2;

        SubMatrix *a00 = split_matrix(A, 0, m, 0, m);
        SubMatrix *a01 = split_matrix(A, 0, m, m, n);
        SubMatrix *a10 = split_matrix(A, m, n, 0, m);
        SubMatrix *a11 = split_matrix(A, m, n, m, n);

        SubMatrix *b00 = split_matrix(B, 0, m, 0, m);
        SubMatrix *b01 = split_matrix(B, 0, m, m, n);
        SubMatrix *b10 = split_matrix(B, m, n, 0, m);
        SubMatrix *b11 = split_matrix(B, m, n, m, n);

        int **c1 = multiply_matrix(a00->matrix, b00->matrix, m, num_processes);
        int **c2 = multiply_matrix(a01->matrix, b10->matrix, m, num_processes);
        int **c3 = multiply_matrix(a00->matrix, b01->matrix, m, num_processes);
        int **c4 = multiply_matrix(a01->matrix, b11->matrix, m, num_processes);
        int **c5 = multiply_matrix(a10->matrix, b00->matrix, m, num_processes);
        int **c6 = multiply_matrix(a11->matrix, b10->matrix, m, num_processes);
        int **c7 = multiply_matrix(a10->matrix, b01->matrix, m, num_processes);
        int **c8 = multiply_matrix(a11->matrix, b11->matrix, m, num_processes);

        combine_results(C, c1, c2, 0, 0);
        combine_results(C, c3, c4, 0, m);
        combine_results(C, c5, c6, m, 0);
        combine_results(C, c7, c8, m, m);

        // Clean up memory
        free(a00);
        free(a01);
        free(a10);
        free(a11);
        free(b00);
        free(b01);
        free(b10);
        free(b11);
    }

    return C;
}

Matrix readMatrixFromFile(const char *filename)
{
    FILE *file = fopen(filename, "r");
    if (!file)
    {
        fprintf(stderr, "Error: Failed to open input file.\n");
        exit(1);
    }
    Matrix result;
    fscanf(file, "%d", &result.n);
    int n = result.n;
    int **A = (int **)malloc(n * sizeof(int *));
    int **B = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++)
    {
        A[i] = (int *)malloc(n * sizeof(int));
        for (int j = 0; j < n; j++)
        {
            fscanf(file, "%d", &A[i][j]);
        }
    }
    for (int i = 0; i < n; i++)
    {
        B[i] = (int *)malloc(n * sizeof(int));
        for (int j = 0; j < n; j++)
        {
            fscanf(file, "%d", &B[i][j]);
        }
    }
    fclose(file);
    result.matrix = A;
    return result;
}

void writeMatrixToFile(const char *filename, int **matrix, int n)
{
    FILE *file = fopen(filename, "w");
    if (!file)
    {
        fprintf(stderr, "Error: Failed to open output file.\n");
        exit(1);
    }
    fprintf(file, "%d\n", n);
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            fprintf(file, "%d ", matrix[i][j]);
        }
        fprintf(file, "\n");
    }
    fclose(file);
}

void free_matrix(int **matrix, int n)
{
    for (int i = 0; i < n; i++)
    {
        free(matrix[i]);
    }
    free(matrix);
}

int main()
{
    const char *input_filename = "big_10_matrices.txt";

    Matrix input_matrix = readMatrixFromFile(input_filename);
    int n = input_matrix.n;
    int **A_matrix = input_matrix.matrix;

    Matrix B_matrix = readMatrixFromFile(input_filename);
    int **B_matrix_data = B_matrix.matrix;

    omp_set_num_threads(8);
    double start_time = omp_get_wtime();
    int **C = multiply_matrix(A_matrix, B_matrix_data, n, 8);
    double elapsed_time = omp_get_wtime() - start_time;

    char output_filename[256];
    snprintf(output_filename, sizeof(output_filename), "%s_%d_output_OpenMP.txt", input_filename, n);
    writeMatrixToFile(output_filename, C, n);

    char info_filename[256];
    snprintf(info_filename, sizeof(info_filename), "%s_%d_info_OpenMP.txt", input_filename, n);
    FILE *info_file = fopen(info_filename, "w");
    if (!info_file)
    {
        fprintf(stderr, "Error: Failed to open info file.\n");
        exit(1);
    }
    fprintf(info_file, "%.2f seconds\n", elapsed_time);
    fclose(info_file);

    // Clean up memory
    free_matrix(A_matrix, n);
    free_matrix(B_matrix_data, n);
    free_matrix(C, n);

    return 0;
}
