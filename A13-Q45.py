# A13-Q45

def inverse_bwt(bwt: str) -> str:
    n = len(bwt)

    # Last column with ranks
    last = []
    occ_count = {}
    for c in bwt:
        occ_count.setdefault(c, 0)
        last.append((c, occ_count[c]))
        occ_count[c] += 1

    # First column = sorted BWT, also with ranks
    first = []
    occ_count_first = {}
    for c in sorted(bwt):
        occ_count_first.setdefault(c, 0)
        first.append((c, occ_count_first[c]))
        occ_count_first[c] += 1

    # Build LF mapping: last_row_index -> first_row_index
    lf_map = {}
    pos_in_first = {}
    for idx, pair in enumerate(first):
        pos_in_first[pair] = idx
    for idx, pair in enumerate(last):
        lf_map[idx] = pos_in_first[pair]

    # Reconstruct string
    res = []
    row = bwt.index("$")     # start where the $ ended up

    for _ in range(n):
        c = bwt[row]
        res.append(c)
        row = lf_map[row]    # follow LF

    # Reverse result (LF walks backwards)
    return "".join(reversed(res))


if __name__ == "__main__":
    import sys
    bwt_input = sys.stdin.read().strip()
    print(inverse_bwt(bwt_input))
