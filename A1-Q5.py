# A1-Q5
p = input()
q = input()


def HammingDistance(p, q):
    if len(p) == len(q):
        d = 0
        for i in range(len(p)):
            if p[i] != q[i]:
                d += 1
            else:
                d += 0
    else:
        return None

    return d


try:
    with open("input.txt", "r") as f:
        p = f.readline().strip()
        q = f.readline().strip()
    result = HammingDistance(p, q)
    if result is None:
        print("Error: Strings must be of equal length")
    else:
        print(result)
except FileNotFoundError:
    print("Error: Input file not found")
except KeyboardInterrupt:
    print("Error: Input interrupted")
