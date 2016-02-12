#!/usr/bin/python

from numpy import *
import operator
import sys

"""
File contains lines like this:
int(miles flown) \t float(hours of game) \t float(litters of icecream) \t ['largeDoses'|'smallDoses'|'didntLike']
e.g. :
40920	8.326976	0.953952	largeDoses
"""
labelNames = { -1 : "didntLike", 0 : "smallDoses", 1 : "largeDoses" }
def parseData(file_in):
    # parse file
    data, labels = [], []
    with open(file_in, 'r') as f:
        try:
            line = f.readline()
            while line:
                fields = line.split()
                data.append([int(fields[0]), float(fields[1]), float(fields[2])])
                label = 1 if (fields[-1] == "largeDoses") else 0 if(fields[-1] == "smallDoses") else -1
                labels.append(label)
                line = f.readline()
        except Exception as e:
            print("Parsing Error!!")
            print(e)

    # homogenize the data
    ad = array(data)
    mins, maxs = ad.min(axis=0), ad.max(axis=0)
    had = (ad - mins) / (maxs - mins)
    return labels, had, mins , maxs

    # compute distances from elt
def classifyEltKNN(labels, had, mins, maxs, elt, k):
    helt = (elt - mins) / (maxs - mins)
    diff = had - helt
    arSqDiff = diff ** 2
    arSsqDiff = arSqDiff.sum(axis=1)
    arRsqDiff = arSsqDiff**0.5

    sortedDistIdx = arRsqDiff.argsort()

    labelsCnt = { l : 0 for l in labels }

    for i in range(min(k, arRsqDiff.size)) :
        labelsCnt[labels[sortedDistIdx[i]]] += 1
    sortedLabelsCnt = sorted( labelsCnt.iteritems(), key=operator.itemgetter(1), reverse=True)

    print(str(sortedLabelsCnt[0][0]) + "  " + labelNames[sortedLabelsCnt[0][0]])


## return label for an element based on its knn in the data
labels, had, mins , maxs = parseData(sys.argv[1])
k = 20
elts = [[400, 0.8, 0.5], [134000, 12, 0.9], [20000, 0, 1.1], [32000, 67, 0.1]]
for elt in elts:
    classifyEltKNN(labels, had, mins , maxs, elt, k)









































