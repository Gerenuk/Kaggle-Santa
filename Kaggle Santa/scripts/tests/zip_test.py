from collections import namedtuple
import csv
import gzip
import io
import pickle
from timeit import timeit

from config import data


Present = namedtuple("Present", "id coor")


def load_csv(file):
    presents = []
    with file as f:
        f.readline()
        for line in csv.reader(f, delimiter=","):
            present = Present(int(line[0]), (int(line[1]), int(line[2]), int(line[3])))
            presents.append(present)
    return presents

presents = load_csv(data.open('presents.csv', newline=''))
presents_pickle = pickle.dumps(presents)

with open("presents.pickle", "wb") as f:
    f.write(presents_pickle)

# print("Raw csv", timeit("presents=load_csv(data.open('presents.csv', newline=''))", setup="from __main__ import load_csv, data", number=5))
# print("Raw pickle", timeit("presents=pickle.load(open('presents.pickle','rb'))", setup="import pickle", number=5))

# for compresslevel in range(10):
#     with gzip.open("packed.gz", "w", compresslevel=compresslevel) as gf:
#         gf.write(data.open('presents.csv', options="rb").read())
#
# #     gf = io.TextIOWrapper(gzip.open('packed.gz', mode='r', compresslevel=compresslevel))
# #     presents2 = load_csv(gf)
# #     print(presents == presents2)
#     print("Gzip{}".format(compresslevel), timeit("presents=load_csv(io.TextIOWrapper(gzip.open('packed.gz', mode='r', compresslevel={})))".format(compresslevel), setup="from __main__ import load_csv, data, gzip, io", number=5))

for compresslevel in range(10):
    with gzip.open("packed.gz", "w", compresslevel=compresslevel) as gf:
        gf.write(presents_pickle)

#     gf = io.TextIOWrapper(gzip.open('packed.gz', mode='r', compresslevel=compresslevel))
#     presents2 = load_csv(gf)
#     print(presents == presents2)
    print("Gzip{}".format(compresslevel), timeit("presents=pickle.load(gzip.open('packed.gz'))".format(compresslevel), setup="from __main__ import pickle, gzip", number=5))

