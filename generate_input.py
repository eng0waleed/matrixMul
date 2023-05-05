# import random

# def generate_matrix(n):
#     return [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]

# def save_matrix_to_file(filename, n, matrix_A, matrix_B):
#     with open(filename, 'w') as f:
#         f.write(f"{n}\n")
#         for row in matrix_A:
#             f.write(" ".join(str(x) for x in row) + "\n")
#         for row in matrix_B:
#             f.write(" ".join(str(x) for x in row) + "\n")

# if __name__ == '__main__':    
#     n = int(input("enter value: "))
#     n = 2**n
#     A_matrix = generate_matrix(n)
#     B_matrix = generate_matrix(n)
#     save_matrix_to_file(f"test_power_{n}_matrices.txt", n, A_matrix, B_matrix)


import random
import concurrent.futures
from math import ceil


def generate_matrix(n):
    return [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]


def save_matrix_to_file(filename, n, matrix_A, matrix_B):
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for row in matrix_A:
            f.write(" ".join(str(x) for x in row) + "\n")
        for row in matrix_B:
            f.write(" ".join(str(x) for x in row) + "\n")


def generate_and_save_matrices(task_id, n, num_processes):
    start = ceil(n * task_id / num_processes)
    end = ceil(n * (task_id + 1) / num_processes)

    for i in range(start, end):
        A_matrix = generate_matrix(2**i)
        B_matrix = generate_matrix(2**i)
        save_matrix_to_file(
            f"test_power_{2**i}_matrices_{task_id}.txt", 2**i, A_matrix, B_matrix)


if __name__ == '__main__':
    n = int(input("enter value: "))
    num_processes = 256

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        tasks = [executor.submit(
            generate_and_save_matrices, i, n, num_processes) for i in range(num_processes)]

    for future in concurrent.futures.as_completed(tasks):
        future.result()
