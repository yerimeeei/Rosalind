# A13-Q47
def preprocess_bwt(bwt):
    """
    Build:
      - FirstOccurrence(symbol)
      - Count(symbol, i) prefix table
    """
    alphabet = sorted(set(bwt))
    first_col = sorted(bwt)

    # FirstOccurrence
    first_occ = {}
    for i, c in enumerate(first_col):
        if c not in first_occ:
            first_occ[c] = i

    # Count table
    count = {c: [0] * (len(bwt) + 1) for c in alphabet}
    for i, ch in enumerate(bwt):
        for c in alphabet:
            count[c][i + 1] = count[c][i]
        count[ch][i + 1] += 1

    return first_occ, count


def bwmatching(bwt, pattern, first_occ, count):
    """
    BWMATCHING from textbook pseudocode (green lines).
    """
    top = 0
    bottom = len(bwt) - 1

    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]

            occ_top = count[symbol][top]
            occ_bottom = count[symbol][bottom + 1]

            if occ_bottom - occ_top > 0:
                top = first_occ[symbol] + occ_top
                bottom = first_occ[symbol] + occ_bottom - 1
            else:
                return 0
        else:
            return bottom - top + 1

    return 0


def main():
    import sys

    # read input file
    infile = sys.argv[1]
    with open(infile, "r") as f:
        data = f.read().strip().split()

    bwt = data[0]
    patterns = data[1:]

    first_occ, count = preprocess_bwt(bwt)

    results = []
    for p in patterns:
        results.append(str(bwmatching(bwt, p, first_occ, count)))

    print(" ".join(results))


if __name__ == "__main__":
    main()
