# A1-Q15
s1 = input()
s2 = input()


# def LongestCommonSubseq(s1, s2):
#     longest = []
#     for i in range(len(s1)-1):
#         for j in range(len(s2)-1):
#             if i == j:
#                 longest.append(i)

def LongestCommonSubseq(s1, s2):
    n, m = len(s1), len(s2)

    # Step 1: Build DP table
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Step 2: Backtrack to get LCS string
    lcs = []
    i, j = n, m
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(lcs))


print(LongestCommonSubseq(s1, s2))  # Expected: AACTGG
