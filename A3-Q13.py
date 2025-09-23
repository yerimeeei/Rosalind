# A1-Q13

money = int(input())
coins = list(map(int, input().split(",")))


# def RecursiveChange(money, coins):
#     if money == 0:
#         return 0
#     MinNumCoins = float('inf')
#     for i in coins:
#         if money >= i:
#             NumCoins = RecursiveChange(money - i, coins)
#             if NumCoins + 1 < MinNumCoins:
#                 MinNumCoins = NumCoins + 1
#     return MinNumCoins


# print(RecursiveChange(money, coins))

def DPChange(money, coins):
    MinNumCoins = {}
    MinNumCoins[0] = 0
    for m in range(1, money + 1):
        MinNumCoins[m] = float('inf')
        for coin in coins:
            if m >= coin:
                if MinNumCoins[m - coin] + 1 < MinNumCoins[m]:
                    MinNumCoins[m] = MinNumCoins[m-coin] + 1
    return MinNumCoins[m]


print(DPChange(money, coins))
