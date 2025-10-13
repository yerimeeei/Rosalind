# A6-Q23
# Find a Topological Ordering of a DAG

def topological_ordering(adj_list):
    from collections import defaultdict, deque

    # Build graph and compute in-degrees
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    nodes = set()

    for line in adj_list:
        if '->' in line:
            parts = line.split('->')
            u = int(parts[0].strip())
            v_list = parts[1].split(',')
            for v_str in v_list:
                v = int(v_str.strip())
                graph[u].append(v)
                in_degree[v] += 1
                nodes.add(v)
            nodes.add(u)
        else:
            # Single node with no outgoing edges
            u = int(line.strip())
            nodes.add(u)
            if u not in graph:
                graph[u] = []

    # Initialize candidates (nodes with zero in-degree)
    candidates = deque([node for node in nodes if in_degree[node] == 0])
    ordering = []

    while candidates:
        a = candidates.popleft()
        ordering.append(a)

        for b in graph[a]:
            in_degree[b] -= 1
            if in_degree[b] == 0:
                candidates.append(b)

        graph[a] = []  # remove edges

    # Check if any edges remain
    if any(graph.values()):
        return "The input graph is not a DAG."
    else:
        return ordering


if __name__ == "__main__":
    adj_list = []
    while True:
        line = input().strip()
        if not line:
            break
        adj_list.append(line)

    ordering = topological_ordering(adj_list)
    if isinstance(ordering, list):
        print(", ".join(map(str, ordering)))
    else:
        print(ordering)
