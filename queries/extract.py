#!/usr/bin/env python
# -*- coding:utf-8 -*-

def from_tsv_get(file_names, delimeter, *args):
    train = []
    test = []
    for file_name in file_names:
        with open(file_name) as tsv:
            #tsv.readline() # first line is general info of file, it shouldn't be there
 
            columns = tsv.readline().split(delimeter) # second line column names
            columns[-1] = columns[-1].replace("\n", "")

            column_indexes = [columns.index(search_term) for search_term in args]
            for line in tsv:
                lis_line = line.split(delimeter)
                lis_line[-1] = lis_line[-1].replace("\n", "")

                if lis_line[column_indexes[1]] == "Added" or lis_line[column_indexes[1]] == "Excluded":
                    train.append([lis_line[col] for col in column_indexes])
                elif lis_line[column_indexes[1]] == "None":
                    test.append([lis_line[col] for col in column_indexes])

    return train, test
 
def hist(lines):
    """
    returns a dictionary each key is a word and each value is a list with relevant and non relevant count.
    """
    temp_words = {}
    pos, neg = 0 ,0

    for l in lines:
        sentiment = (l[1] == 'Added' or l[2] == "1") and (not l[1] == 'Excluded')
        if sentiment:
            pos += 1
        else:
            neg += 1

    for line in lines:
        sentiment = (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded')

        query = set(line[0].split())

        for w in query:
            if w in temp_words:
                if sentiment:

                    temp_words[w][0] += 1
                    temp_words[w][2] -= 1
                else:
                    temp_words[w][1] += 1
                    temp_words[w][3] -= 1

            else:
                if sentiment:
                    temp_words[w] = [1, 0, pos - 1, neg]
                else:
                    temp_words[w] = [0, 1, pos, neg - 1]
    return temp_words

 
def rel_non_rel_lines(lines):
    pos = 0
    neg = 0
    for line in lines:
        if (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded'):
            pos += 1
        else:
            neg += 1
    return [pos, neg]
 
 
def totalNumOfWords(words):
    pos = 0
    neg = 0
    for word in words.itervalues():
        pos += word[0]
        neg += word[1]
 
    return [pos, neg]