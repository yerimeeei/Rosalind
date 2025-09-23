# A1-Q14

def read_input():  # from ChatGPT
    # first line: n and m
    n, m = map(int, input().split())

    # Down matrix: n rows, m+1 columns
    Down = []
    for _ in range(n):
        Down.append(list(map(int, input().split())))

    # separator '-'
    sep = input().strip()
    assert sep == "-"

    # Right matrix: n+1 rows, m columns
    Right = []
    for _ in range(n+1):
        Right.append(list(map(int, input().split())))

    return n, m, Down, Right


n, m, Down, Right = read_input()


def LengthLongestPath(n, m):
    Grid = [[0]*(m+1) for _ in range(n+1)]
    if n == 0 and m == 0:
        return 0
    if n > 0 and m > 0:
        # initialize first column from ChatGPT
        for i in range(1, n+1):
            Grid[i][0] = Grid[i-1][0] + Down[i-1][0]

        # initialize first row from ChatGPT
        for j in range(1, m+1):
            Grid[0][j] = Grid[0][j-1] + Right[0][j-1]

        for i in range(1, n+1):
            for j in range(1, m+1):
                Grid[i][j] = max(Grid[i-1][j] + Down[i-1][j],
                                 Grid[i][j-1] + Right[i][j-1])
        return Grid[n][m]


print(LengthLongestPath(n, m))
