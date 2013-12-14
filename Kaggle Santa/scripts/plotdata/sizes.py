from load.load import presents
import matplotlib.pyplot as plt

edges=list(sorted(p.coor) for p in presents)
coor=list(zip(*edges))

plt.hist(coor, bins=50)
plt.legend(["min", "med", "max"])
plt.ylabel("Number")
plt.xlabel("Edge")
plt.show()

