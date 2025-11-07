# A10-Q32
# Compute Distances Between Leaves

def read_input():
    n = int(input("").strip())
    print("")

    graph = {}
    while True:
        line = input()
        if not line.strip():
            break
        src, rest = line.split("->")
        dst, weight = rest.split(":")
        src, dst, weight = int(src), int(dst), int(weight)
        if src not in graph:
            graph[src] = []
        graph[src].append((dst, weight))
    return n, graph


def dfs(graph, start, target, visited):
    """Return distance from start to target using DFS."""
    if start == target:
        return 0
    visited.add(start)
    for nxt, w in graph.get(start, []):
        if nxt not in visited:
            dist = dfs(graph, nxt, target, visited)
            if dist is not None:
                return w + dist
    return None


def compute_leaf_distances(n, graph):
    leaves = list(range(n))
    dist_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = dfs(graph, i, j, set())
    return dist_matrix


def main():
    n, graph = read_input()
    dist_matrix = compute_leaf_distances(n, graph)
    print("\n")
    for row in dist_matrix:
        print(' '.join(map(str, row)))


if __name__ == "__main__":
    main()
