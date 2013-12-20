from collections import Counter
import itertools
import functools
import operator
import matplotlib.pyplot as plt

from load.load import presents
presents = presents()

volumes = [functools.reduce(operator.mul, p.coor, 1) for p in presents]
count = Counter(volumes)
x, y = zip(*sorted(count.items()))
plt.scatter(x, y)
plt.show()
