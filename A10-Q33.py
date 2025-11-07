# A10-Q33
# Compute Limb Lengths in a Tree

def limb_length(n, j, D):
    limb_len = float("inf")
    for i in range(n):
        if i == j:
            continue
        for k in range(n):
            if k == j or k == i:
                continue
            # Formula: (Di,j + Dj,k - Di,k) / 2
            length = (D[i][j] + D[j][k] - D[i][k]) / 2
            if length < limb_len:
                limb_len = length
    return int(limb_len)


def read_input():
    n = int(input("").strip())
    j = int(input("").strip())
    print("")
    D = []
    for _ in range(n):
        row = list(map(int, input().split()))
        D.append(row)
    return n, j, D


def main():
    n, j, D = read_input()
    print("\nLimb Length of leaf", j, "is:", limb_length(n, j, D))


if __name__ == "__main__":
    main()
