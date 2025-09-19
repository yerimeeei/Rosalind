# A2-Q8

import sys


def profile_most_probable_kmer(text, k, profile):
    max_prob = -1
    most_prob_kmer = text[0:k]

    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        prob = 1
        for j, nucleotide in enumerate(kmer):
            if nucleotide == 'A':
                prob *= profile[0][j]
            elif nucleotide == 'C':
                prob *= profile[1][j]
            elif nucleotide == 'G':
                prob *= profile[2][j]
            elif nucleotide == 'T':
                prob *= profile[3][j]
        if prob > max_prob:
            max_prob = prob
            most_prob_kmer = kmer
    return most_prob_kmer


lines = sys.stdin.read().splitlines()
text = lines[0].strip()
k = int(lines[1].strip())
profile = [list(map(float, line.split())) for line in lines[2:6]]

print(profile_most_probable_kmer(text, k, profile))
