# A11-Q37
# Implement SmallParsimony

import sys
import math
from collections import defaultdict

# -----------------------------
# Utility: parse and build tree
# -----------------------------


def parse_input(lines):
    n = int(lines[0])
    edges = []
    for line in lines[1:]:
        u, v = line.strip().split("->")
        edges.append((u.strip(), v.strip()))
    return n, edges


def build_tree(edges):
    children = defaultdict(list)
    parents = {}
    leaf_labels = {}
    nodes = set()

    for u, v in edges:
        nodes.add(u)
        # leaf edge has string (A,C,G,T)
        if all(ch in "ACGT" for ch in v):
            leaf_labels[u + "_" + v] = v  # temporary key unique
            nodes.add(u + "_" + v)
            children[u].append(u + "_" + v)
            parents[u + "_" + v] = u
        else:
            children[u].append(v)
            parents[v] = u
            nodes.add(v)

    # find root
    root = next(node for node in nodes if node not in parents)
    return children, root, leaf_labels, nodes


# -----------------------------
# Small Parsimony core
# -----------------------------
def small_parsimony(tree, root, leaf_labels):
    alphabet = ['A', 'C', 'G', 'T']
    sk = {}
    tag = {}

    for v in tree:
        tag[v] = 0
    for v in leaf_labels:
        tag[v] = 1
        sk[v] = {a: 0 if a == leaf_labels[v] else math.inf for a in alphabet}

    while True:
        ripe_nodes = [v for v in tree if tag[v] ==
                      0 and all(tag[c] == 1 for c in tree[v])]
        if not ripe_nodes:
            break

        for v in ripe_nodes:
            tag[v] = 1
            l, r = tree[v]
            sk[v] = {}
            for k in alphabet:
                left_min = min(sk[l][a] + (0 if a == k else 1)
                               for a in alphabet)
                right_min = min(sk[r][b] + (0 if b == k else 1)
                                for b in alphabet)
                sk[v][k] = left_min + right_min

    # get minimum score
    score = min(sk[root].values())

    # Backtrack to assign characters
    labels = {}

    def assign_label(v, parent_label=None):
        if v in leaf_labels:
            labels[v] = leaf_labels[v]
            return
        if parent_label is None:
            best = min(sk[v], key=sk[v].get)
        else:
            best = min(sk[v], key=lambda a: sk[v][a] +
                       (0 if a == parent_label else 1))
        labels[v] = best
        for c in tree[v]:
            assign_label(c, best)

    assign_label(root)
    return score, labels


# -----------------------------
# Run per-position and combine
# -----------------------------
def run_small_parsimony_on_dna(n, edges):
    children, root, leaf_labels, nodes = build_tree(edges)
    k = len(next(iter(leaf_labels.values())))
    score_total = 0
    internal_labels = {v: [''] * k for v in nodes if v not in leaf_labels}

    for i in range(k):
        # extract per-position base for each leaf
        char_labels = {v: seq[i] for v, seq in leaf_labels.items()}
        score, labels = small_parsimony(children, root, char_labels)
        score_total += score
        for v in labels:
            if v in internal_labels:
                internal_labels[v][i] = labels[v]

    # join reconstructed sequences
    full_labels = {**leaf_labels}
    for v in internal_labels:
        full_labels[v] = ''.join(internal_labels[v])

    return score_total, children, full_labels


# -----------------------------
# Main execution
# -----------------------------
def main():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    n, edges = parse_input(lines)
    score, tree, labels = run_small_parsimony_on_dna(n, edges)

    def hamming(a, b):
        return sum(x != y for x, y in zip(a, b))

    print(score)
    printed = set()
    for u in tree:
        for v in tree[u]:
            if (v, u) not in printed:
                print(
                    f"{labels[u]}->{labels[v]}:{hamming(labels[u], labels[v])}")
                print(
                    f"{labels[v]}->{labels[u]}:{hamming(labels[u], labels[v])}")
                printed.add((u, v))


if __name__ == "__main__":
    main()
