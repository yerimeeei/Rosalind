# A1-Q4
text = input()
k = int(input())


def findkmer(text, k):
    dic = dict()
    for i in range(len(text)):
        m = text[i:i+k]
        dic[m] = dic.get(m, 0) + 1

    max_count = max(dic.values())
    most_frequent = [kmer for kmer, count in dic.items() if count == max_count]

    return most_frequent


result = findkmer(text, k)
print(" ".join(result))
