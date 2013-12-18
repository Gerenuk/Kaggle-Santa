from collections import Counter
import itertools
import matplotlib.pyplot as plt

from load.load import presents


edges = list(tuple(sorted(p.coor)) for p in presents)

SHIFT = 30

count = Counter()
for i in range(len(edges)):
    for edge in edges[i]:
        for nextedge in itertools.chain.from_iterable(edges[i + 1:i + 1 + SHIFT]):
            count[edge + nextedge] += 1

x, y = zip(*sorted(count.items()))
plt.plot(x, y)
plt.show()
