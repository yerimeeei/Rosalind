# A10-Q34
# Implement AdditivePhylogeny

def limb_length(D, j):
    """Compute limb length for leaf j (0-based in current D)."""
    n = len(D)
    best = float("inf")
    for i in range(n):
        if i == j:
            continue
        for k in range(n):
            if k == j or k == i:
                continue
            val = (D[i][j] + D[j][k] - D[i][k]) / 2
            if val < best:
                best = val
    return best


def add_edge(G, a, b, w):
    G.setdefault(a, []).append((b, w))
    G.setdefault(b, []).append((a, w))


def remove_edge(G, a, b, w):
    G[a].remove((b, w))
    G[b].remove((a, w))


def find_path(G, start, end, visited=None):
    """Return list of nodes from start to end (DFS)."""
    if visited is None:
        visited = set()
    if start == end:
        return [start]
    visited.add(start)
    for nxt, _w in G.get(start, []):
        if nxt not in visited:
            p = find_path(G, nxt, end, visited)
            if p:
                return [start] + p
    return []


def insert_node_on_path(G, u, v, x, next_id):
    """
    Ensure there is a node at distance x from u along the path u->v.
    Return (node_at_x, updated_next_id).
    """
    path = find_path(G, u, v)
    if not path:
        raise ValueError(f"No path between {u} and {v}.")

    dist = 0.0
    for a, b in zip(path, path[1:]):
        # find weight of edge (a,b)
        w = next(w for (nbr, w) in G[a] if nbr == b)
        if abs(dist + w - x) < 1e-8:
            return b, next_id  # exactly on existing node
        if dist < x < dist + w:
            # split edge (a,b)
            new_node = next_id
            next_id += 1
            add_edge(G, new_node, a, x - dist)
            add_edge(G, new_node, b, dist + w - x)
            remove_edge(G, a, b, w)
            return new_node, next_id
        dist += w

    raise ValueError(f"x={x} beyond path length between {u} and {v}.")


def additive_phylogeny_core(D, labels, next_id):
    """
    D: current distance matrix (list of lists)
    labels: mapping of local indices (0..len(D)-1) -> global leaf labels (0..N-1)
    next_id: next available internal-node id (>= N)
    Returns (graph, next_id)
    """
    n = len(D)
    if n == 2:
        G = {}
        a, b = labels[0], labels[1]
        add_edge(G, a, b, D[0][1])
        return G, next_id

    j = n - 1
    limb = limb_length(D, j)
    # adjust last column/row by limb
    for i in range(n - 1):
        D[i][j] -= limb
        D[j][i] = D[i][j]

    # find i,k with D[i][k] = D[i][j] + D[j][k]
    i = k = None
    for a in range(n - 1):
        for b in range(n - 1):
            if a == b:
                continue
            if abs(D[a][b] - (D[a][j] + D[j][b])) < 1e-8:
                i, k = a, b
                break
        if i is not None:
            break
    if i is None:
        raise ValueError(
            "No (i,k) satisfying D[i,k] = D[i,j] + D[j,k]. Is D additive?")

    x = D[i][j]  # distance from leaf i to the attachment point along path i->k

    # recurse on matrix with j-th leaf removed
    D_trim = [row[:-1] for row in D[:-1]]
    labels_trim = labels[:-1]
    G, next_id = additive_phylogeny_core(D_trim, labels_trim, next_id)

    # map local indices to global labels for insertion
    gi, gk, gj = labels[i], labels[k], labels[j]

    # ensure a node at distance x from gi along path gi->gk
    v, next_id = insert_node_on_path(G, gi, gk, x, next_id)

    # attach leaf gj with limb length
    add_edge(G, v, gj, limb)
    return G, next_id


def additive_phylogeny(D):
    """Wrapper that initializes labels and next_id correctly."""
    N = len(D)
    labels = list(range(N))   # leaves keep their original labels 0..N-1
    next_id = N               # first internal node id
    # Deep-copy D to avoid modifying caller's matrix
    D_copy = [row[:] for row in D]
    G, _ = additive_phylogeny_core(D_copy, labels, next_id)
    return G


def read_input():
    n = int(input("Enter number of leaves (n): ").strip())
    print("Enter the distance matrix (space/tab separated):")
    vals = []
    while len(vals) < n * n:
        line = input().strip()
        if not line:
            continue
        vals.extend(map(int, line.split()))
    D = [vals[i*n:(i+1)*n] for i in range(n)]
    return D


def main():
    D = read_input()
    G = additive_phylogeny(D)
    print("\nWeighted adjacency list:")
    for src in sorted(G.keys()):
        for dst, w in G[src]:
            print(f"{src}->{dst}:{int(round(w))}")


if __name__ == "__main__":
    main()
