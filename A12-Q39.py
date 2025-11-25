# A12-Q39
# Construct the Suffix Tree of a String
Text = "ACGAGGCCACTTGCCACAGAGCACCCGGAAGGCTCTTAGATTAGTAAAGGAGAGCGGAATACTGTGTCTGGTAATATTAATGCTCGCGCTCGGGCCAAGGCTTACAACTTGCCTGAAAACCAGAAATATTACTAGTCGTGACTTGGAGACTATCTTCAAGTTCTTGTGGAAGAACGAAACGACATCAATGTTACTAAGATAGGCATAATTGGGGATTAGTAGAATGATTGCAGATTCCGGATGCGCCTGGTTTCATATTTCCGCAACACACCTCCAGGTGCGATAAGTAGGTCATTCAATTACGGGGCTACGTAGAAGTTTTATAACGAAACCACGAGACGGACCGGACATTTCCCTGCAACAGGTACTGACATTGCCATATCTTTCGCACCGGACCAAATATCCACTCCGTTTGATGAAAATAGACGCTCTCACGCCTGATGGGTACATGTTAACCCGTTGATAGTATCTGCTACTGATAAGCGACCCGCGAACGATGTGCGAGAGTTCGGAAATTCTATAACTTGCCAAGTCATCAATCTCATTATCTTTGGACCGGGCTTAGGTACCAACCGGTGTGAGTACGACCTGATTCACAACCCTGTAGTAATAAAATTTCGAACAGCTACCGCAGCGGTCTGGAGATAACCACTTTATCCATTAGGGTAGAGCGAAGTCAACAACGCAACATGCTTAAAGGATTGGTTTGCGGAACCTGGGTAGTGATTGTGGGATATACCAGTCGGACTTCAGTCATCTGAAACTTTCGATTTATCCGCTATTCTTAATCTCGCAACGCAAGCTCTGAATGACGCTACCCGTTTGCTGTCTAGATGTGGGGCCTAGCGTACCGCAC$"
output_file = "/Users/rimi/Desktop/suffix_tree_output.txt"


# ---------- suffix array ----------
def build_suffix_array(s):
    return sorted(range(len(s)), key=lambda i: s[i:])


# ---------- Kasai LCP ----------
def build_lcp(s, sa):
    n = len(s)
    rank = [0] * n
    for i, v in enumerate(sa):
        rank[v] = i

    h = 0
    lcp = [0] * (n - 1)

    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank[i] - 1] = h
            if h > 0:
                h -= 1
    return lcp


# ---------- Build Suffix Tree edges ----------
def suffix_tree_edges(s):
    sa = build_suffix_array(s)
    lcp = build_lcp(s, sa)

    # Node stack: (string_depth, start, end)
    stack = [(0, None, None)]
    edges = []

    for i in range(len(sa)):
        suffix_start = sa[i]
        cur_lcp = lcp[i - 1] if i > 0 else 0

        # pop until top depth <= cur_lcp
        while stack[-1][0] > cur_lcp:
            stack.pop()

        # parent node info
        parent_depth, parent_start, parent_end = stack[-1]

        # edge for new leaf
        edge_start = suffix_start + cur_lcp
        edge_end = len(s)
        edges.append(s[edge_start:edge_end])

        # push leaf node with its depth
        leaf_depth = len(s) - suffix_start
        stack.append((leaf_depth, edge_start, edge_end))

    return edges


# ------- Write output to file -------
def main():
    edges = suffix_tree_edges(Text)

    with open(output_file, "w") as f:
        for e in edges:
            f.write(e + "\n")

    print(f"Suffix tree edges written to:\n{output_file}")


if __name__ == "__main__":
    main()
