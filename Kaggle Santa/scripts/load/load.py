from collections import namedtuple
import csv

from config import data


Present=namedtuple("Present", "id coor")
    
presents=[]
with data.open("presents.csv", newline="") as f:
    f.readline()
    for line in csv.reader(f, delimiter=","):
        present=Present(int(line[0]),(int(line[1]),int(line[2]),int(line[3])))
        presents.append(present)
        #print(present)

#change