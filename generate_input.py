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
    _n = int(input("enter power value: "))
    n = 2**_n
    A_matrix = generate_matrix(n)
    B_matrix = generate_matrix(n)
    # save_matrix_to_file(f"test_power_{n}_matrices.txt", n, A_matrix, B_matrix)
    save_matrix_to_file(f"test_power_{_n}_matrices.txt", n, A_matrix, B_matrix)



# import random
# import concurrent.futures


# def generate_row(n):
#     return [random.randint(1, 10) for _ in range(n)]


# def save_matrix_to_file(filename, n, matrix_A, matrix_B):
#     with open(filename, 'w') as f:
#         f.write(f"{n}\n")
#         for row in matrix_A:
#             f.write(" ".join(str(x) for x in row) + "\n")
#         for row in matrix_B:
#             f.write(" ".join(str(x) for x in row) + "\n")


# def generate_matrix_parallel(n, num_processes):
#     with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
#         matrix = list(executor.map(generate_row, [n] * n))
#     return matrix


# if __name__ == '__main__':
#     _n = int(input("enter value: "))
#     n = 2**_n
#     num_processes = 450

#     A_matrix = generate_matrix_parallel(n, num_processes)
#     B_matrix = generate_matrix_parallel(n, num_processes)
#     save_matrix_to_file(f"test_power_{_n}_matrices.txt", n, A_matrix, B_matrix)
