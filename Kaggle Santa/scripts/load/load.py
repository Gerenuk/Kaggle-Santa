from collections import namedtuple
import csv

from config import data


Present=namedtuple("Present", "id coor")
    
presents=[]
with data.open("presents.csv", newline="") as f:
    f.readline()
    for line in csv.reader(f, delimiter=","):
        present=Present(line[0],(line[1],line[2],line[3]))
        presents.append(present)
        #print(present)