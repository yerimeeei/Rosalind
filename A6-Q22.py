# A6-Q22
# Align Two Strings using Affine Gap Penalties
import sys
import numpy as np

BLOSUM62 = {
    'A': {'A': 4, 'C': 0, 'D': -2, 'E': -1, 'F': -2, 'G': 0, 'H': -2, 'I': -1, 'K': -1, 'L': -1, 'M': -1, 'N': -2, 'P': -1, 'Q': -1, 'R': -1, 'S': 1, 'T': 0, 'V': 0, 'W': -3, 'Y': -2},
    'C': {'A': 0, 'C': 9, 'D': -3, 'E': -4, 'F': -2, 'G': -3, 'H': -3, 'I': -1, 'K': -3, 'L': -1, 'M': -1, 'N': -3, 'P': -3, 'Q': -3, 'R': -3, 'S': -1, 'T': -1, 'V': -1, 'W': -2, 'Y': -2},
    'D': {'A': -2, 'C': -3, 'D': 6, 'E': 2, 'F': -3, 'G': -1, 'H': -1, 'I': -3, 'K': -1, 'L': -4, 'M': -3, 'N': 1, 'P': -1, 'Q': 0, 'R': -2, 'S': 0, 'T': -1, 'V': -3, 'W': -4, 'Y': -3},
    'E': {'A': -1, 'C': -4, 'D': 2, 'E': 5, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 1, 'L': -3, 'M': -2, 'N': 0, 'P': -1, 'Q': 2, 'R': 0, 'S': 0, 'T': -1, 'V': -2, 'W': -3, 'Y': -2},
    'F': {'A': -2, 'C': -2, 'D': -3, 'E': -3, 'F': 6, 'G': -3, 'H': -1, 'I': 0, 'K': -3, 'L': 0, 'M': 0, 'N': -3, 'P': -4, 'Q': -3, 'R': -3, 'S': -2, 'T': -2, 'V': -1, 'W': 1, 'Y': 3},
    'G': {'A': 0, 'C': -3, 'D': -1, 'E': -2, 'F': -3, 'G': 6, 'H': -2, 'I': -4, 'K': -2, 'L': -4, 'M': -3, 'N': 0, 'P': -2, 'Q': -2, 'R': -2, 'S': 0, 'T': -2, 'V': -3, 'W': -2, 'Y': -3},
    'H': {'A': -2, 'C': -3, 'D': -1, 'E': 0, 'F': -1, 'G': -2, 'H': 8, 'I': -3, 'K': -1, 'L': -3, 'M': -2, 'N': 1, 'P': -2, 'Q': 0, 'R': 0, 'S': -1, 'T': -2, 'V': -3, 'W': -2, 'Y': 2},
    'I': {'A': -1, 'C': -1, 'D': -3, 'E': -3, 'F': 0, 'G': -4, 'H': -3, 'I': 4, 'K': -3, 'L': 2, 'M': 1, 'N': -3, 'P': -3, 'Q': -3, 'R': -3, 'S': -2, 'T': -1, 'V': 3, 'W': -3, 'Y': -1},
    'K': {'A': -1, 'C': -3, 'D': -1, 'E': 1, 'F': -3, 'G': -2, 'H': -1, 'I': -3, 'K': 5, 'L': -2, 'M': -1, 'N': 0, 'P': -1, 'Q': 1, 'R': 2, 'S': 0, 'T': -1, 'V': -2, 'W': -3, 'Y': -2},
    'L': {'A': -1, 'C': -1, 'D': -4, 'E': -3, 'F': 0, 'G': -4, 'H': -3, 'I': 2, 'K': -2, 'L': 4, 'M': 2, 'N': -3, 'P': -3, 'Q': -2, 'R': -2, 'S': -2, 'T': -1, 'V': 1, 'W': -2, 'Y': -1},
    'M': {'A': -1, 'C': -1, 'D': -3, 'E': -2, 'F': 0, 'G': -3, 'H': -2, 'I': 1, 'K': -1, 'L': 2, 'M': 5, 'N': -2, 'P': -2, 'Q': 0, 'R': -1, 'S': -1, 'T': -1, 'V': 1, 'W': -1, 'Y': -1},
    'N': {'A': -2, 'C': -3, 'D': 1, 'E': 0, 'F': -3, 'G': 0, 'H': 1, 'I': -3, 'K': 0, 'L': -3, 'M': -2, 'N': 6, 'P': -2, 'Q': 0, 'R': 0, 'S': 1, 'T': 0, 'V': -3, 'W': -4, 'Y': -2},
    'P': {'A': -1, 'C': -3, 'D': -1, 'E': -1, 'F': -4, 'G': -2, 'H': -2, 'I': -3, 'K': -1, 'L': -3, 'M': -2, 'N': -2, 'P': 7, 'Q': -1, 'R': -2, 'S': -1, 'T': -1, 'V': -2, 'W': -4, 'Y': -3},
    'Q': {'A': -1, 'C': -3, 'D': 0, 'E': 2, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 1, 'L': -2, 'M': 0, 'N': 0, 'P': -1, 'Q': 5, 'R': 1, 'S': 0, 'T': -1, 'V': -2, 'W': -2, 'Y': -1},
    'R': {'A': -1, 'C': -3, 'D': -2, 'E': 0, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 2, 'L': -2, 'M': -1, 'N': 0, 'P': -2, 'Q': 1, 'R': 5, 'S': -1, 'T': -1, 'V': -3, 'W': -3, 'Y': -2},
    'S': {'A': 1, 'C': -1, 'D': 0, 'E': 0, 'F': -2, 'G': 0, 'H': -1, 'I': -2, 'K': 0, 'L': -2, 'M': -1, 'N': 1, 'P': -1, 'Q': 0, 'R': -1, 'S': 4, 'T': 1, 'V': -2, 'W': -3, 'Y': -2},
    'T': {'A': 0, 'C': -1, 'D': -1, 'E': -1, 'F': -2, 'G': -2, 'H': -2, 'I': -1, 'K': -1, 'L': -1, 'M': -1, 'N': 0, 'P': -1, 'Q': -1, 'R': -1, 'S': 1, 'T': 5, 'V': 0, 'W': -2, 'Y': -2},
    'V': {'A': 0, 'C': -1, 'D': -3, 'E': -2, 'F': -1, 'G': -3, 'H': -3, 'I': 3, 'K': -2, 'L': 1, 'M': 1, 'N': -3, 'P': -2, 'Q': -2, 'R': -3, 'S': -2, 'T': 0, 'V': 4, 'W': -3, 'Y': -1},
    'W': {'A': -3, 'C': -2, 'D': -4, 'E': -3, 'F': 1, 'G': -2, 'H': -2, 'I': -3, 'K': -3, 'L': -2, 'M': -1, 'N': -4, 'P': -4, 'Q': -2, 'R': -3, 'S': -3, 'T': -2, 'V': -3, 'W': 11, 'Y': 2},
    'Y': {'A': -2, 'C': -2, 'D': -3, 'E': -2, 'F': 3, 'G': -3, 'H': 2, 'I': -1, 'K': -2, 'L': -1, 'M': -1, 'N': -2, 'P': -3, 'Q': -1, 'R': -2, 'S': -2, 'T': -2, 'V': -1, 'W': 2, 'Y': 7}
}

GAP_OPEN = 11
GAP_EXTEND = 1
v = input("").strip()
w = input("").strip()

# --- Helper function for substitution score ---


def blosum_score(a, b):
    # safely get score from nested dictionary
    try:
        return BLOSUM62[a][b]
    except KeyError:
        # fallback if amino acid not in dictionary
        if a == b:
            return 4  # typical match score
        else:
            return -1  # typical mismatch score

# --- Affine gap alignment ---


def affine_gap_alignment(v, w):
    n = len(v)
    m = len(w)

    # Initialize matrices
    M = [[-float('inf')] * (m+1) for _ in range(n+1)]  # match/mismatch
    Ix = [[-float('inf')] * (m+1) for _ in range(n+1)]  # gap in v
    Iy = [[-float('inf')] * (m+1) for _ in range(n+1)]  # gap in w

    # Traceback matrices
    TB_M = [[None]*(m+1) for _ in range(n+1)]
    TB_Ix = [[None]*(m+1) for _ in range(n+1)]
    TB_Iy = [[None]*(m+1) for _ in range(n+1)]

    # Base cases
    M[0][0] = 0
    for i in range(1, n+1):
        Ix[i][0] = -GAP_OPEN - (i-1)*GAP_EXTEND
        TB_Ix[i][0] = 'Ix'
    for j in range(1, m+1):
        Iy[0][j] = -GAP_OPEN - (j-1)*GAP_EXTEND
        TB_Iy[0][j] = 'Iy'

    # Fill matrices
    for i in range(1, n+1):
        for j in range(1, m+1):
            # M matrix
            scores = [M[i-1][j-1], Ix[i-1][j-1], Iy[i-1][j-1]]
            best_prev = max(scores)
            M[i][j] = best_prev + blosum_score(v[i-1], w[j-1])
            if best_prev == M[i-1][j-1]:
                TB_M[i][j] = 'M'
            elif best_prev == Ix[i-1][j-1]:
                TB_M[i][j] = 'Ix'
            else:
                TB_M[i][j] = 'Iy'

            # Ix matrix (gap in v)
            scores = [M[i-1][j]-GAP_OPEN, Ix[i-1][j]-GAP_EXTEND]
            Ix[i][j] = max(scores)
            TB_Ix[i][j] = 'M' if scores[0] >= scores[1] else 'Ix'

            # Iy matrix (gap in w)
            scores = [M[i][j-1]-GAP_OPEN, Iy[i][j-1]-GAP_EXTEND]
            Iy[i][j] = max(scores)
            TB_Iy[i][j] = 'M' if scores[0] >= scores[1] else 'Iy'

    # Start traceback from the max of M[n][m], Ix[n][m], Iy[n][m]
    matrices = [M[n][m], Ix[n][m], Iy[n][m]]
    max_score = max(matrices)
    if max_score == M[n][m]:
        matrix = 'M'
    elif max_score == Ix[n][m]:
        matrix = 'Ix'
    else:
        matrix = 'Iy'

    # Traceback
    aligned_v = []
    aligned_w = []
    i, j = n, m

    while i > 0 or j > 0:
        if matrix == 'M':
            prev = TB_M[i][j]
            aligned_v.append(v[i-1])
            aligned_w.append(w[j-1])
            i -= 1
            j -= 1
            matrix = prev
        elif matrix == 'Ix':
            prev = TB_Ix[i][j]
            aligned_v.append(v[i-1])
            aligned_w.append('-')
            i -= 1
            matrix = prev
        elif matrix == 'Iy':
            prev = TB_Iy[i][j]
            aligned_v.append('-')
            aligned_w.append(w[j-1])
            j -= 1
            matrix = prev

    aligned_v = ''.join(reversed(aligned_v))
    aligned_w = ''.join(reversed(aligned_w))

    return max_score, aligned_v, aligned_w


# --- Run alignment ---
score, aligned_v, aligned_w = affine_gap_alignment(v, w)
print(score)
print(aligned_v)
print(aligned_w)
