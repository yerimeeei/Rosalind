# A2-Q12

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


def kmer_probability(kmer, profile):
    prob = 1
    for i, nucleotide in enumerate(kmer):
        prob *= profile[nucleotide][i]
    return prob


def profile_randomly_generated_kmer(text, k, profile):
    n = len(text) - k + 1
    kmers = [text[i:i+k] for i in range(n)]
    probs = [kmer_probability(kmer, profile) for kmer in kmers]
    total = sum(probs)
    if total == 0:
        probs = [1/n]*n  # uniform fallback
    else:
        probs = [p/total for p in probs]

    return random.choices(kmers, weights=probs, k=1)[0]


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


def gibbs_sampler(Dna, k, t, N):
    Motifs = [dna[random.randint(0, len(dna)-k):][:k] for dna in Dna]
    BestMotifs = list(Motifs)

    for _ in range(N):
        i = random.randint(0, t-1)
        Motifs_except_i = Motifs[:i] + Motifs[i+1:]
        prof = profile_with_pseudocounts(Motifs_except_i)
        Motifs[i] = profile_randomly_generated_kmer(Dna[i], k, prof)
        if score(Motifs) < score(BestMotifs):
            BestMotifs = list(Motifs)
    return BestMotifs


def gibbs_sampler_multiple_starts(Dna, k, t, N, starts=20):
    BestOverall = None
    for _ in range(starts):
        Motifs = gibbs_sampler(Dna, k, t, N)
        if BestOverall is None or score(Motifs) < score(BestOverall):
            BestOverall = Motifs
    return BestOverall


if __name__ == "__main__":
    lines = sys.stdin.read().splitlines()
    k, t, N = map(int, lines[0].split())
    Dna = [line.strip() for line in lines[1:] if line.strip()]

    BestMotifs = gibbs_sampler_multiple_starts(Dna, k, t, N, starts=20)

    print("\n".join(BestMotifs))
