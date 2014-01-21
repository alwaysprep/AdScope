# -*- coding:utf-8 -*-
from collections import defaultdict
import itertools
import math


def from_tsv_get(file_name, *args):
    with open(file_name) as tsv:
        tsv.readline() # first line is general info of file, it shouldn't be there

        columns = tsv.readline().split("\t") # second line column names
        columns[-1] = columns[-1].replace("\n", "")

        column_indexes = [columns.index(search_term) for search_term in args]

        for line in tsv:
            lis_line = line.split("\t")
            lis_line[-1] = lis_line[-1].replace("\n", "")
            yield [lis_line[col] for col in column_indexes]


def rel_hist(lines):
    for line in lines:
        if (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded'):
            yield line[0].split()

def non_rel_hist(lines):
    for line in lines:
        if (line[1] != "Added" and line[2] == "0") or (line[1] == 'Excluded'):
            yield line[0].split()


def rsv(query, fil):
    words = query.split()
    lines1, lines2 = itertools.tee(from_tsv_get(fil, 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'), 2)
    rel_words, non_rel_words = rel_hist(lines1), non_rel_hist(lines2)
    rel_dict = defaultdict(int)
    non_rel_dict = defaultdict(int)
    rsv = {}
    rel_total = 0
    non_rel_total = 0
    for word in words:
        for line in rel_words:
            rel_total += 1
            if word in line:
                rel_dict[word] += 1

        for line in non_rel_words:
            non_rel_total += 1
            if word in line:
                non_rel_dict[word] += 1


        rsv[word] = {
            "positive": rel_dict[word],
            "negative": non_rel_dict[word],
            "absent_positive": rel_total - rel_dict[word],
            "absent_negative": non_rel_total - non_rel_dict[word]
        }

    return rsv

def calculateC(word, fil):
    table = rsv(word, fil)
    return math.log(((table[word]["positive"] + 0.5 ) / (table[word]["absent_positive"] + 0.5)) / (
        ( table[word]["negative"] + 0.5 ) / (table[word]["absent_negative"] + 0.5)))


def calculateRsv(query, fil):
    sentence = query.split(" ")
    total = 0
    for word in sentence:
        total = total + calculateC(word, fil)
    return total


if __name__ == "__main__":
    #print rsv("ning", "data/data.tsv")

    print calculateRsv("what ning", "data/data.tsv")




