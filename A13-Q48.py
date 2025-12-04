# A13-Q48

def preprocess_bwt(bwt: str):
    """
    Preprocess BWT to build:
    - FirstOccurrence: dict[char] -> first index in sorted(bwt)
    - Count: dict[char] -> list where Count[c][i] = # of c in bwt[0:i]
    """
    n = len(bwt)
    alphabet = sorted(set(bwt))

    # Build FirstOccurrence from sorted BWT (the "first column")
    first_column = ''.join(sorted(bwt))
    first_occurrence = {}
    for i, c in enumerate(first_column):
        if c not in first_occurrence:
            first_occurrence[c] = i

    # Initialize Count table
    count = {c: [0] * (n + 1) for c in alphabet}

    # Fill Count[c][i]
    for i, c in enumerate(bwt, start=1):
        # copy previous counts
        for ch in alphabet:
            count[ch][i] = count[ch][i - 1]
        # increment for current symbol
        count[c][i] += 1

    return first_occurrence, count


def better_bw_matching(bwt: str, pattern: str, first_occurrence, count) -> int:
    """
    BETTERBWMATCHING(FirstOccurrence, LastColumn, Pattern, Count)
    Returns number of matches of pattern in Text given BWT(Text) = bwt.
    """
    top = 0
    bottom = len(bwt) - 1

    # Quick membership check
    if pattern and any(c not in first_occurrence for c in pattern):
        return 0

    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]

            if symbol not in first_occurrence:
                return 0

            count_top = count[symbol][top]
            count_bottom = count[symbol][bottom + 1]

            if count_bottom - count_top > 0:
                top = first_occurrence[symbol] + count_top
                bottom = first_occurrence[symbol] + count_bottom - 1
            else:
                return 0
        else:
            return bottom - top + 1

    return 0


def better_bw_matching_all(bwt: str, patterns):
    first_occurrence, count = preprocess_bwt(bwt)
    return [better_bw_matching(bwt, p, first_occurrence, count) for p in patterns]


if __name__ == "__main__":
    import sys

    # read from an input.txt file instead of stdin
    infile = sys.argv[1]
    with open(infile, "r") as f:
        data = f.read().strip().split()

    bwt = data[0]
    patterns = data[1:]

    counts = better_bw_matching_all(bwt, patterns)
    print(" ".join(map(str, counts)))
