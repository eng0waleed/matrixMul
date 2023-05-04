import random

def generate_matrix(n):
    return [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]

def save_matrix_to_file(filename, n, matrix_A, matrix_B):
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for row in matrix_A:
            f.write(" ".join(str(x) for x in row) + "\n")
        for row in matrix_B:
            f.write(" ".join(str(x) for x in row) + "\n")

if __name__ == '__main__':
    n = 2**9
    A_matrix = generate_matrix(n)
    B_matrix = generate_matrix(n)
    save_matrix_to_file("big_9_matrices.txt", n, A_matrix, B_matrix)
