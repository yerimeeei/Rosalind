# A2-Q10

import sys


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


def greedy_motif_search_with_pseudocounts(Dna, k, t):
    BestMotifs = [dna[:k] for dna in Dna]
    first_string = Dna[0]

    for i in range(len(first_string) - k + 1):
        Motifs = []
        Motif1 = first_string[i:i+k]
        Motifs.append(Motif1)

        for j in range(1, t):
            profile = profile_with_pseudocounts(Motifs)
            next_motif = profile_most_probable_kmer(Dna[j], k, profile)
            Motifs.append(next_motif)

        if score(Motifs) < score(BestMotifs):
            BestMotifs = Motifs

    return BestMotifs


if __name__ == "__main__":
    lines = sys.stdin.read().splitlines()
    k, t = map(int, lines[0].split())
    Dna = [line.strip() for line in lines[1:] if line.strip()]

    BestMotifs = greedy_motif_search_with_pseudocounts(Dna, k, t)

    print("\n".join(BestMotifs))
