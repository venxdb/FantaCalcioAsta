test = {
    "Marco": 10,
    "Steefano": 56,
    "Michele": 31
}

test = sorted(test.items(), key = lambda x: x[1])

print(test)