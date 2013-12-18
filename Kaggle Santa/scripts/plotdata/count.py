from collections import Counter
import itertools
import matplotlib.pyplot as plt

from load.load import presents


edges = list(tuple(sorted(p.coor)) for p in presents)

x, y = zip(*list(Counter(itertools.chain.from_iterable(edges)).items()))
plt.scatter(x, y)
plt.show()
