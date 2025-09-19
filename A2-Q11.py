# A2-Q11

import sys
import random


def profile_with_pseudocounts(motifs):
    k = len(motifs[0])
    profile = {'A': [1]*k, 'C': [1]*k, 'G': [1]*k, 'T': [1]*k}

    for j in range(k):
        for motif in motifs:
            profile[motif[j]][j] += 1

    t = len(motifs) + 4
    for j in range(k):
        for nucleotide in 'ACGT':
            profile[nucleotide][j] /= t
    return profile


def profile_most_probable_kmer(text, k, profile):
    max_prob = -1
    most_prob_kmer = text[:k]
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        prob = 1
        for j, nucleotide in enumerate(kmer):
            prob *= profile[nucleotide][j]
        if prob > max_prob:
            max_prob = prob
            most_prob_kmer = kmer
    return most_prob_kmer


def score(motifs):
    k = len(motifs[0])
    t = len(motifs)
    total_score = 0
    for j in range(k):
        counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
        for i in range(t):
            counts[motifs[i][j]] += 1
        total_score += t - max(counts.values())
    return total_score


def randomized_motif_search_once(Dna, k, t):
    # Randomly select initial motifs
    Motifs = [dna[random.randint(0, len(dna)-k):][:k] for dna in Dna]
    BestMotifs = list(Motifs)

    while True:
        profile = profile_with_pseudocounts(Motifs)
        Motifs = [profile_most_probable_kmer(dna, k, profile) for dna in Dna]
        if score(Motifs) < score(BestMotifs):
            BestMotifs = list(Motifs)
        else:
            return BestMotifs


def randomized_motif_search(Dna, k, t, N=1000):
    BestOverall = None
    for _ in range(N):
        Motifs = randomized_motif_search_once(Dna, k, t)
        if BestOverall is None or score(Motifs) < score(BestOverall):
            BestOverall = Motifs
    return BestOverall


if __name__ == "__main__":
    lines = sys.stdin.read().splitlines()
    k, t = map(int, lines[0].split())
    Dna = [line.strip() for line in lines[1:] if line.strip()]

    BestMotifs = randomized_motif_search(Dna, k, t, N=1000)

    print("\n".join(BestMotifs))
