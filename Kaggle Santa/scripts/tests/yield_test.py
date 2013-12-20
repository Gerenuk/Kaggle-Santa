def test():
    yield 1
    return 3
    yield 2

print(list(test()))
