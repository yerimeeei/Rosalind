# A8-Q30
# Implement the Soft k-Means Clustering Algorithm

import sys
import numpy as np


def read_input():
    lines = sys.stdin.read().strip().splitlines()
    k, m = map(int, lines[0].split())
    beta = float(lines[1])
    data = np.array([list(map(float, line.split())) for line in lines[2:]])
    return k, m, beta, data


def euclidean_distance(p1, p2):
    """Compute Euclidean distance between two vectors."""
    return np.linalg.norm(p1 - p2)


def soft_kmeans(k, m, beta, data, iterations=100):
    n = data.shape[0]
    centers = data[:k].copy()

    for step in range(iterations):
        hidden = np.zeros((k, n))
        for i in range(k):
            for j in range(n):
                dist = euclidean_distance(data[j], centers[i])
                hidden[i, j] = np.exp(-beta * dist)
        # normalize across all centers for each data point
        hidden /= hidden.sum(axis=0, keepdims=True)

        for i in range(k):
            # weighted sum of data points
            numerator = np.dot(hidden[i], data)
            denominator = hidden[i].sum()
            centers[i] = numerator / denominator

    return centers


def main():
    k, m, beta, data = read_input()
    centers = soft_kmeans(k, m, beta, data)
    for center in centers:
        print(" ".join(f"{x:.3f}" for x in center))


if __name__ == "__main__":
    main()
