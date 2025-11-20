# A11-Q36
# Implement the Neighbor Joining Algorithm
import sys
import numpy as np


def neighbor_joining(D, n, node_ids=None, next_node=None):
    if node_ids is None:
        node_ids = list(range(n))
    if next_node is None:
        next_node = n

    # Base case
    if n == 2:
        i, j = node_ids[0], node_ids[1]
        T = {i: [(j, D[0, 1])], j: [(i, D[0, 1])]}
        return T, next_node

    # Row sums (total distance per taxon)
    total_dist = D.sum(axis=1)

    # Q (neighbor-joining) matrix
    D_prime = np.full_like(D, np.inf, dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j:
                D_prime[i, j] = (n - 2) * D[i, j] - \
                    total_dist[i] - total_dist[j]

    # Choose pair (i,j) minimizing Q
    flat_idx = np.argmin(D_prime)
    i, j = divmod(flat_idx, n)

    # Limb lengths
    delta = (total_dist[i] - total_dist[j]) / (n - 2)
    limb_i = 0.5 * (D[i, j] + delta)
    limb_j = 0.5 * (D[i, j] - delta)

    # Distances from new node m to others
    new_row = []
    for k in range(n):
        if k != i and k != j:
            dkm = 0.5 * (D[i, k] + D[j, k] - D[i, j])
            new_row.append(dkm)
    new_row = np.array(new_row, dtype=float)

    # Build reduced matrix with new node
    mask = np.ones(n, dtype=bool)
    mask[[i, j]] = False
    D_new = D[mask][:, mask]
    D_new = np.vstack([D_new, new_row])
    D_new = np.column_stack([D_new, np.append(new_row, 0.0)])

    # Update labels
    node_ids_new = [node_ids[k]
                    for k in range(n) if k not in (i, j)] + [next_node]

    # Recurse
    T, next_node = neighbor_joining(D_new, n - 1, node_ids_new, next_node + 1)

    # Connect new internal node m to original i and j
    m = node_ids_new[-1]
    ni, nj = node_ids[i], node_ids[j]
    for a, b, w in [(m, ni, limb_i), (m, nj, limb_j)]:
        T.setdefault(a, []).append((b, w))
        T.setdefault(b, []).append((a, w))

    return T, next_node


def print_tree(T):
    for a in sorted(T.keys()):
        for b, w in T[a]:
            print(f"{a}->{b}:{w:.3f}")


if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin if line.strip()]
    n = int(lines[0])
    D = np.array([list(map(float, l.split())) for l in lines[1:]], dtype=float)
    tree, _ = neighbor_joining(D, n)
    print_tree(tree)
