# A7-Q28
# Compute the Squared Error Distortion

import math
import sys


def distance(p1, p2):
    """Compute Euclidean distance between two m-dimensional points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def distortion(Data, Centers):
    """Compute squared error distortion."""
    total = 0.0
    n = len(Data)

    for point in Data:
        # find nearest center
        min_dist = min(distance(point, c) for c in Centers)
        total += min_dist ** 2

    return total / n


def main():
    # Read input (handles stdin or file redirect)
    lines = [line.strip() for line in sys.stdin if line.strip()]

    # Find separator line (--------)
    sep_index = None
    for i, line in enumerate(lines):
        if set(line) == {"-"}:
            sep_index = i
            break

    # Parse input
    k, m = map(int, lines[0].split())
    Centers = [list(map(float, line.split())) for line in lines[1:sep_index]]
    Data = [list(map(float, line.split())) for line in lines[sep_index+1:]]

    # Compute distortion
    result = distortion(Data, Centers)

    # Print with 3 decimal places
    print(f"{result:.3f}")


if __name__ == "__main__":
    main()
