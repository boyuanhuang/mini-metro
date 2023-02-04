# Floyd Warshall Algorithm in python


# Algorithm implementation
def floyd_warshall(G):
    distance = list(map(lambda i: list(map(lambda j: j, i)), G))

    # Adding vertices individually
    for k in range(nV):
        for i in range(nV):
            for j in range(nV):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
    print_solution(distance)


# Printing the solution
def print_solution(distance):
    for i in range(nV):
        for j in range(nV):
            if (distance[i][j] == INF):
                print("INF", end=" ")
            else:
                print(distance[i][j], end="  ")
        print(" ")


# # The number of vertices
nV = 4

INF = 999

G = [[0, 3, INF, 5],
     [2, 0, INF, 4],
     [INF, 1, 0, INF],
     [INF, INF, 2, 0]]

floyd_warshall(G)


class A:

    def __init__(self):
        self.a = 1
        self.B = None

    def update_B(self, B):
        self.B = B

    def __del__(self):
        print('deleting A')

    def self_destruct(self):
        del self



class B:
    def __init__(self, A):
        self.b = 2
        self.A = A

    def __del__(self):
        print('deleting B')


if __name__ == '__main__':
    def test(n):
        return n%2 == 0

    if not test(2):
        print(1)
    else:
        print(2)

