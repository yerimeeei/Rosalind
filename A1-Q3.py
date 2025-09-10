# A1-Q3
text = input()
pattern = input()


def PatternCount(text, pattern):
    count = 0
    for i in range(len(text) - len(pattern) + 1):
        if text[i: i+len(pattern)] == pattern:
            count += 1
            i += len(pattern) - 1
    return count


print(PatternCount(text, pattern))
