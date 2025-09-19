# A2-Q6

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


def appears_in_string(pattern, text, d):
    k = len(pattern)
    for i in range(len(text) - k + 1):
        substring = text[i:i+k]
        if HammingDistance(pattern, substring) <= d:
            return True
    return False

# from Chat-GPT


def neighbors(pattern, d):
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return {"A", "C", "G", "T"}

    suffix_neighbors = neighbors(pattern[1:], d)
    neighborhood = set()
    for text in suffix_neighbors:
        if HammingDistance(pattern[1:], text) < d:
            for nucleotide in "ACGT":
                neighborhood.add(nucleotide + text)
        else:
            neighborhood.add(pattern[0] + text)
    return neighborhood


def MotifEnumeration(Dna, k, d):
    patterns = set()
    for text in Dna:
        for i in range(len(text) - k + 1):
            kmer = text[i:i+k]
            # from here Chat-GPT
            for neighbor in neighbors(kmer, d):
                if all(appears_in_string(neighbor, other, d) for other in Dna):
                    patterns.add(neighbor)
    return patterns


lines = sys.stdin.read().splitlines()
k, d = map(int, lines[0].split())
Dna = lines[1:]

result = sorted(MotifEnumeration(Dna, k, d))
print(" ".join(result))
