# A13-Q46

def last_to_first(transform: str, i: int) -> int:
    # Build LAST column with ranks
    last = []
    occ_last = {}
    for c in transform:
        occ_last.setdefault(c, 0)
        last.append((c, occ_last[c]))
        occ_last[c] += 1

    # Build FIRST column with ranks (sorted LAST)
    first = []
    occ_first = {}
    for c in sorted(transform):
        occ_first.setdefault(c, 0)
        first.append((c, occ_first[c]))
        occ_first[c] += 1

    # Map each (char, rank) in FIRST to its index
    first_index = {}
    for idx, pair in enumerate(first):
        first_index[pair] = idx

    # LAST[i] tells us the pair we must find
    pair = last[i]

    # Position in FIRST column
    return first_index[pair]


if __name__ == "__main__":
    import sys

    lines = sys.stdin.read().strip().split()
    transform = lines[0]
    i = int(lines[1])

    print(last_to_first(transform, i))
