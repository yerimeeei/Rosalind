# A10-Q35
# Implement UPGMA

def read_input():
    n = int(input("Enter number of taxa (n): ").strip())
    print("Enter the distance matrix (space/tab separated):")
    vals = []
    # Read until we have n*n numbers, so line wrapping is fine
    while len(vals) < n * n:
        line = input().strip()
        if not line:
            continue
        vals.extend(map(float, line.split()))
    M = [vals[i*n:(i+1)*n] for i in range(n)]
    return n, M


def build_dist_dict(M):
    """Convert static matrix to dict-of-dicts keyed by cluster id."""
    n = len(M)
    dist = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = M[i][j]
    return dist


def upgma(M):
    n = len(M)
    dist = build_dist_dict(M)
    # Active clusters: ids start at 0..n-1 for leaves
    active = set(range(n))
    size = {i: 1 for i in range(n)}     # cluster sizes
    age = {i: 0.0 for i in range(n)}    # node ages
    next_id = n                         # next internal node label

    # Undirected adjacency list: node -> list of (neighbor, length)
    graph = {i: [] for i in range(n)}

    def add_edge(u, v, w):
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))

    while len(active) > 1:
        # Find closest pair (i, j) among active clusters
        min_d = float("inf")
        i = j = None
        act_list = sorted(active)
        for a_idx in range(len(act_list)):
            a = act_list[a_idx]
            for b_idx in range(a_idx + 1, len(act_list)):
                b = act_list[b_idx]
                d = dist[a][b]
                if d < min_d:
                    min_d = d
                    i, j = a, b

        # Create new cluster id
        new = next_id
        next_id += 1
        # Age of the new node is half the intercluster distance
        age[new] = min_d / 2.0

        # Connect new node to i and j; edge lengths are age(new) - age(child)
        add_edge(new, i, age[new] - age[i])
        add_edge(new, j, age[new] - age[j])

        # Prepare distances from 'new' to every other active cluster k
        dist[new] = {}
        for k in list(active):
            if k in (i, j):
                continue
            # UPGMA average:
            d_new_k = (size[i] * dist[i][k] + size[j] *
                       dist[j][k]) / (size[i] + size[j])
            dist[new][k] = d_new_k
            dist[k][new] = d_new_k

        # Update cluster size
        size[new] = size[i] + size[j]

        # Remove i, j from distance dicts
        for k in list(active):
            if k in (i, j):
                continue
            dist[k].pop(i, None)
            dist[k].pop(j, None)
        dist.pop(i, None)
        dist.pop(j, None)

        # Remove i, j from active; add new
        active.remove(i)
        active.remove(j)
        active.add(new)

        # Make sure graph has entries for internal node
        graph.setdefault(new, [])

    return graph


def print_graph(graph):
    # Print adjacency list with three decimal places
    for src in sorted(graph.keys()):
        for dst, w in graph[src]:
            print(f"{src}->{dst}:{w:.3f}")


def main():
    n, M = read_input()
    G = upgma(M)
    print("\nAdjacency list:")
    print_graph(G)


if __name__ == "__main__":
    main()
