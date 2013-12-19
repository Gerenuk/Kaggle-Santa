import functools
import operator

from load.load import presents


print(sum(functools.reduce(operator.mul, p.coor, 1) for p in presents))
