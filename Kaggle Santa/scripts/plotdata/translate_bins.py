from collections import Counter
import functools
import itertools
from operator import itemgetter
import operator
from pprint import pprint
import matplotlib.pyplot as plt

from load.load import presents
presents = presents()

def mapping(x):
    if x <= 4:
        return 0
    if x <= 10:
        return 1
    if x <= 45:
        return 2
    if x <= 64:
        return 3
    if x <= 70:
        return 4
    if x <= 100:
        return 5
    return 6

mapped = [tuple(map(mapping, sorted(p.coor))) for p in presents]
mapped2 = [(p.coor, tuple(map(mapping, sorted(p.coor)))) for p in presents]
count = Counter(mapped)

keys = set(count.keys())
allkeys = set(tuple(sorted(x)) for x in itertools.product(range(7), repeat=3))
pprint(sorted(allkeys - keys))
pprint(sorted(tuple(sorted(x, reverse=True) for x in allkeys - keys), reverse=True))

thresh = [4, 10, 45, 64, 70, 100, 250]

def stats(coor):
    a, b, c = thresh[coor[0]], thresh[coor[1]], thresh[coor[2]]
    return (a * b * c, a * b, b * c, a * c)

pprint(sorted([(coor in keys, coor, stats(coor), count[coor]) for coor in allkeys], key=itemgetter(1)))

def keyrange(x, y):
    return set(tuple(sorted(x)) for x in itertools.product(range(x, y + 1), repeat=3))

def keyrange2(x1, y1, x2, y2, x3, y3):
    return set(tuple(sorted(x)) for x in itertools.product(range(x1, y1 + 1), range(x2, y2 + 1), range(x3, y3 + 1)))

testkeys = keyrange(0, 2) | keyrange(1, 4) | keyrange(4, 6) | keyrange2(1, 2, 1, 2, 5, 5)

pprint(testkeys - keys)
pprint(keys - testkeys)

def correct(key, num):
    # return int(num / len(set(itertools.permutations(key))) * functools.reduce(operator.mul, [{1:0.5, 2:1 / 12, 4:0.62, 3:1 / 5, 5:5}.get(x, 1) for x in key], 1))
    return int(1000 * num / len(set(itertools.permutations(key))) * functools.reduce(operator.mul, [{0:1 / 3, 1:1 / 6, 2:1 / 35, 3:1 / 19, 4:1 / 6, 5:1 / 30, 6:1 / 150}.get(x, 1) for x in key], 1))

x = sorted((key, count[key], correct(key, count[key])) for key in keys)
pprint(x)


scores = {key:correct(key, count[key]) for key in keys}

keys2 = [(m[0], scores[m[1]]) for m in mapped2]

# pprint([tuple(sorted(coor)) for coor, score in keys2 if max(coor) <= 10][:100])
