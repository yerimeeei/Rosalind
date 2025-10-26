# A8-Q31
# Implement Hierarchical Clustering

import sys
import numpy as np


def read_input():
    """Read n and nxn distance matrix from stdin."""
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    values = list(map(float, data[1:]))
    D = np.array(values).reshape((n, n))
    return n, D


def hierarchical_clustering(n, D):
    clusters = {i: [i] for i in range(n)}  # cluster label → members
    next_label = n
    history = []

    while len(clusters) > 1:
        # find two closest clusters by average distance
        min_dist = float("inf")
        closest_pair = None
        keys = list(clusters.keys())

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                c1, c2 = keys[i], keys[j]
                members1, members2 = clusters[c1], clusters[c2]
                dists = [D[x, y] for x in members1 for y in members2]
                avg_dist = sum(dists) / len(dists)
                if avg_dist < min_dist:
                    min_dist = avg_dist
                    closest_pair = (c1, c2)

        i, j = closest_pair
        new_cluster = next_label
        next_label += 1

        # merge clusters preserving order: Ci first, then Cj
        clusters[new_cluster] = clusters[i] + clusters[j]
        history.append(clusters[new_cluster])

        # compute Davg distances for new cluster
        new_row = []
        for c in clusters.keys():
            if c in (i, j, new_cluster):
                continue
            members1, members2 = clusters[new_cluster], clusters[c]
            dists = [D[x, y] for x in members1 for y in members2]
            Davg = sum(dists) / len(dists)
            new_row.append((c, Davg))

        # remove merged clusters
        del clusters[i]
        del clusters[j]

        # extend distance matrix
        D = np.pad(D, ((0, 1), (0, 1)), constant_values=0)
        for c, dist in new_row:
            D[new_cluster, c] = D[c, new_cluster] = dist

    return history


def main():
    n, D = read_input()
    results = hierarchical_clustering(n, D)
    for cluster in results:
        # convert to 1-based indices
        print(" ".join(str(x + 1) for x in cluster))


if __name__ == "__main__":
    main()
