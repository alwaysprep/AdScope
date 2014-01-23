#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rsv import from_tsv_get, calculateRsv
from bigram import get_prob_of_query

def rsv_test(line, fil):
    pass


def bigram_test(line, fil):
    pass

def test(training, test, func):
    training_data = from_tsv_get(training, 'Search term', 'Added/Excluded', 'Conv. (1-per-click)')
    test_data = from_tsv_get(test, 'Search term', 'Added/Excluded', 'Conv. (1-per-click)')
    total_rsv = 0
    total_bigram = 0

    for line in test_data:

        if rsv_test(line, "data/data.tsv"):
            total_rsv += 1

        if bigram_test(line, "data/data.tsv"):
            total_bigram += 1

    return "rsv: " + str(total_rsv) + " bigram: " + str(total_bigram)


if __name__ == "__main__":
    file = from_tsv_get(("data/data.tsv",), 'Search term', 'Added/Excluded', 'Conv. (1-per-click)')
    lis = []
    for line in file:
        lis.append((get_prob_of_query(line[0], "data/data.tsv"), calculateRsv(line[0], "data/data.tsv"), line[0]))
    lis.sort()

    for element in lis:
        print "%.5f, %.5f, %s" % (element[0], element[1], element[2])