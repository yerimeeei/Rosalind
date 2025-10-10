# A4-Q16
# Find the Longest Path in a DAG
from collections import defaultdict, deque
import sys


def longest_path_dag(source, sink, edges):
    # Step 1: Build graph and indegree count
    graph = defaultdict(list)
    indegree = defaultdict(int)
    nodes = set()

    for edge in edges:
        u, rest = edge.split("->")
        v, w = rest.split(":")
        u, v, w = int(u), int(v), int(w)
        graph[u].append((v, w))
        indegree[v] += 1
        nodes.add(u)
        nodes.add(v)

    # Step 2: Topological sort (Kahn’s algorithm)
    q = deque([node for node in nodes if indegree[node] == 0])
    topo_order = []
    while q:
        u = q.popleft()
        topo_order.append(u)
        for v, _ in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    # Step 3: Longest path DP
    dist = {node: float("-inf") for node in nodes}
    dist[source] = 0
    parent = {}

    for u in topo_order:
        for v, w in graph[u]:
            if dist[u] + w > dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    # Step 4: Backtrack path
    path = []
    cur = sink
    while cur != source:
        path.append(cur)
        cur = parent[cur]
    path.append(source)
    path.reverse()

    return dist[sink], path


if __name__ == "__main__":
    data = sys.stdin.read().strip().splitlines()
    source = int(data[0])
    sink = int(data[1])
    edges = data[2:]

    length, path = longest_path_dag(source, sink, edges)
    print(length)
    print("->".join(map(str, path)))
