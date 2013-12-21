from collections import namedtuple
import csv
import pickle
from operator import attrgetter

from config import data


Present = namedtuple("Present", "id coor")


def load_csv(file):
    result = []
    with file as f:
        f.readline()
        for line in csv.reader(f, delimiter=","):
            present = Present(int(line[0]), (int(line[1]), int(line[2]), int(line[3])))
            result.append(present)
            # print(present)
    return result

# presents = load_csv(data.open("presents.csv", newline=""))

# pickle.dump(presents, data.open("presents.pickle", options="wb"))


def presents():
    Present = namedtuple("Present", "id coor")
    return sorted(pickle.load(data.open("presents.pickle", options="rb")), key=attrgetter("id"))

# change
