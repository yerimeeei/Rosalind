# A2-Q7

import sys
from itertools import product


def HammingDistance(p, q):
    if len(p) == len(q):
        d = 0
        for i in range(len(p)):
            if p[i] != q[i]:
                d += 1
            else:
                d += 0
    else:
        return None

    return d


def d_pattern_text(pattern, text):
    k = len(pattern)
    min_dist = float("inf")
    for i in range(len(text) - k + 1):
        substring = text[i:i+k]
        dist = HammingDistance(pattern, substring)
        if dist < min_dist:
            min_dist = dist
    return min_dist


def d_pattern_dna(pattern, Dna):
    return sum(d_pattern_text(pattern, dna) for dna in Dna)


def all_kmers(k):
    return ["".join(p) for p in product("ACGT", repeat=k)]


def median_string(Dna, k):
    best_pattern = None
    best_distance = float("inf")

    for pattern in all_kmers(k):
        dist = d_pattern_dna(pattern, Dna)
        if dist < best_distance:
            best_distance = dist
            best_pattern = pattern
    return best_pattern


lines = sys.stdin.read().splitlines()
k = int(lines[0])
Dna = lines[1:]

print(median_string(Dna, k))
