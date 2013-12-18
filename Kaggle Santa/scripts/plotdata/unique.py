from collections import Counter
from load.load import presents


edges = list(tuple(sorted(p.coor)) for p in presents)

count = Counter((a, b, c) for a, b, c in edges if a > 10 or b > 10 or c > 10)

