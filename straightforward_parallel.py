
from multiprocessing import Pool
from time import time

def StraightDivAndConqP(A, B):
    n = len(A)
    C = [[0]*n]*n
    start = time()
    pool = Pool(processes=n)
    C = pool.map(multiply_straightforward, [(A, B, i, n) for i in range(n)])
    end = time()
    print('Time taken: ', end - start)
    return C

def multiply_straightforward(args):
    A, B, i, n = args
    print(i)
    return [sum([A[i][k] * B[k][j] for k in range(n)]) for j in range(n)]

def read_matrix(filename):
    with open(filename, 'r') as f:
        n = int(f.readline())
        setMatrixDimentions(n)
        A = [[0 for i in range(n)] for j in range(n)]
        B = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            A[i] = [int(x) for x in f.readline().split()]
        for i in range(n):
            B[i] = [int(x) for x in f.readline().split()]
        return A, B

A_matrix = []
B_matrix = []


def setMatrixDimentions(n):
    global n_value
    n_value = n

#write a main function to run the functions
if __name__ == '__main__':
    A_matrix, B_matrix = read_matrix('myfile.txt')
    C_matrix = StraightDivAndConqP(A_matrix, B_matrix)
    with open('result.txt', 'w') as f:
        f.write(str(n_value) + '\n')
        for i in range(n_value):
            for j in range(n_value):
                f.write(str(C_matrix[i][j]) + ' ')
            f.write('\n')