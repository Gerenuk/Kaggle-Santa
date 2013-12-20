from collections import Counter

from load.load import presents
import matplotlib.pyplot as plt
presents = presents()

edges = list(sorted(p.coor) for p in presents)
coor = list(zip(*edges))

x, y = zip(*sorted(Counter(coor[0] + coor[1] + coor[2]).items()))

plt.plot(x, y)
# plt.legend(["min", "med", "max"])
plt.ylabel("Number")
plt.xlabel("Edge")
plt.show()

