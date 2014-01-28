#!/usr/bin/env python
# -*- coding:utf-8 -*-

def from_tsv_get(file_names, delimeter, *args):
    for file_name in file_names:
        with open(file_name) as tsv:
            #tsv.readline() # first line is general info of file, it shouldn't be there

            columns = tsv.readline().split(delimeter) # second line column names
            columns[-1] = columns[-1].replace("\n", "")

            column_indexes = [columns.index(search_term) for search_term in args]

            for line in tsv:
                lis_line = line.split(delimeter)
                lis_line[-1] = lis_line[-1].replace("\n", "")
                yield [lis_line[col] for col in column_indexes]




def hist(words, lines):
    for line in lines:
        if (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded'):
            sentiment = True
        else:
            sentiment = False

        query = line[0].split()
        for word in query:
            if word not in words:
                if sentiment:
                    words[word] = [1, 0]
                else:
                    words[word] = [0, 1]
            else:
                if sentiment:
                    words[word][0] += 1
                else:
                    words[word][1] += 1

def get_adjacents(couples, line):

    if (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded'):
        sentiment = True
    else:
        sentiment = False
    query = line[0].split()

    for index in xrange(len(query)-1):
        if (query[index], query[index + 1]) not in couples:
            if sentiment:
                couples[(query[index], query[index + 1])] = [1, 0]
            else:
                couples[(query[index], query[index + 1])] = [0, 1]
        else:
            if sentiment:
                couples[(query[index], query[index + 1])][0] += 1
            else:
                couples[(query[index], query[index + 1])][1] += 1



def couple_hist(couples, lines):
    for line in lines:
        get_adjacents(couples, line)


def rel_non_rel_lines(lines):
    pos = 0
    neg = 0
    for line in lines:
        if (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded'):
            pos += 1
        else:
            neg += 1
    return [pos, neg]

