# A7-Q29
# Implement the Lloyd Algorithm for k-Means Clustering

import math
import sys


def distance(p1, p2):
    """Compute Euclidean distance between two m-dimensional points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def mean(points):
    """Compute the mean point of a list of points."""
    m = len(points[0])
    n = len(points)
    return [sum(p[i] for p in points) / n for i in range(m)]


def assign_clusters(Data, Centers):
    """Assign each point in Data to the nearest center."""
    clusters = [[] for _ in Centers]
    for point in Data:
        # Find index of the nearest center
        distances = [distance(point, c) for c in Centers]
        nearest_center = distances.index(min(distances))
        clusters[nearest_center].append(point)
    return clusters


def lloyd(Data, k):
    """Perform the Lloyd algorithm (k-Means)."""
    Centers = Data[:k]  # First k points as initial centers

    while True:
        clusters = assign_clusters(Data, Centers)

        # Recompute centers as mean of clusters
        new_Centers = []
        for cluster in clusters:
            if len(cluster) > 0:
                new_Centers.append(mean(cluster))
            else:
                # Handle empty cluster by keeping the old center
                new_Centers.append(Centers[len(new_Centers)])

        # Check for convergence
        if all(math.isclose(distance(Centers[i], new_Centers[i]), 0, abs_tol=1e-6)
               for i in range(k)):
            break
        Centers = new_Centers

    return Centers


def main():
    # Read input from stdin
    lines = [line.strip() for line in sys.stdin if line.strip()]
    k, m = map(int, lines[0].split())
    Data = [list(map(float, line.split())) for line in lines[1:]]

    Centers = lloyd(Data, k)

    for center in Centers:
        print(' '.join(f"{coord:.3f}" for coord in center))


if __name__ == "__main__":
    main()
