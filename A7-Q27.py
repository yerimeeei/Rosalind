# A7-Q27
# Implement FarthestFirstTraversal

import math
import sys


def d(p1, p2):
    """Euclidean distance between two m-dimensional points."""
    distance_squared = 0.0
    for i in range(len(p1)):  # len(p1) == m
        distance_squared += (p2[i] - p1[i]) ** 2
    return math.sqrt(distance_squared)


def FarthestFirstTraversal(Data, k):
    """Implements Farthest-First Traversal starting from the first point."""
    Centers = [Data[0]]  # first point, not random

    while len(Centers) < k:
        # For each point, find its distance to the nearest center
        distances = []
        for point in Data:
            min_dist = min(d(point, c) for c in Centers)
            distances.append(min_dist)

        # Choose the point with the largest min_dist
        max_index, _ = max(enumerate(distances), key=lambda x: x[1])
        Centers.append(Data[max_index])

    return Centers


def main():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    # m is number of dimensions, used implicitly
    k, m = map(int, lines[0].split())

    # Read all m-dimensional points
    Data = [list(map(float, line.split())) for line in lines[1:]]

    Centers = FarthestFirstTraversal(Data, k)

    for center in Centers:
        print(' '.join(map(str, center)))


if __name__ == "__main__":
    main()
