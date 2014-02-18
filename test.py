#!/usr/bin/env python
# -*- coding:utf-8 -*-
from extract import from_tsv_get, hist, rel_non_rel_lines, get_tf
import math
from rsv import calculateRsv, calculateC
from config import rsv_threshold, rsv_smoothing_factor
from nltk.corpus import wordnet
#import matplotlib.pyplot as plt
import numpy as np
from stemming import stem_file

def extract_data(fil, sf=None):
    lines = list(from_tsv_get((fil,), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))
    words = hist(lines)
    lins = rel_non_rel_lines(lines)
    idf = get_tf(lines)
    for word in words:
            words.get(word).extend([calculateC(word, words, lins, sf), idf[word]])

    return words, lins, lines

def isEnglish(sentence, words):
    sentenceList = sentence.split()
    for word in sentenceList:
        if not wordnet.synsets(word) :
            if sum(words.get(word,[0,0])[:2]) < 3:
                return False
    return True

def sixty_char(sentence):
    return sentence + " " * (60 - len(sentence))



def get_precision(rsv_threshold, sf):
    files = ["first", "second", "third", "fourth", "fifth", "sixth"]
    total = 0
    for fil in files:
        rsv = 0
        words, lins, lines = extract_data("data/train/" + fil + "Train.csv", sf)

        test = list(from_tsv_get(("data/test/" + fil + "Test.csv",), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))
        for line in test:

            sentiment = (line[1] == "Added" or line[2] == "1") and ( not line[1] == "Excluded" )

            rsv_sentiment = (calculateRsv(line[0], words, lins) > rsv_threshold) and isEnglish(line[0], words)
            if rsv_sentiment == sentiment:
                rsv += 1

        total += rsv
    return (total) / 3390.0


def grid(sf, rt):
    for s in sf:
        for r in rt:
            a = get_precision(round(r,1), round(s,2))
            print a
            yield a


def prec_tfidf(x):
    files = ["first", "second", "third", "fourth", "fifth", "sixth"]
    total = 0
    for fil in files:
        rsv = 0

        words, lins, lines = extract_data("data/train/" + fil + "Train.csv")

        test = list(from_tsv_get(("data/test/" + fil + "Test.csv",), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))

        other250 = sorted([(word[1][3] * math.log(float(len(lines))/sum(word[1][:2])), word[0]) for word in words.items()])[::-1][x:]

        for other in other250:
            words[other[1]][2] = 0

        for line in test:
            sentiment = (line[1] == "Added" or line[2] == "1") and ( not line[1] == "Excluded" )

            rsv_sentiment = (calculateRsv(line[0], words, lins) > rsv_threshold) and isEnglish(line[0], words)

            if rsv_sentiment == sentiment:
                rsv += 1

        total += rsv
    return total/ 3390.0

if __name__ == "__main__":
    """

    print("rsv     rsvFalse   total")

    files = ["first", "second", "third", "fourth", "fifth", "sixth"]

    for fil in files:
        rsv = 0
        queries = ""
        words, lins, lines = extract_data("data/train/" + fil + "Train_stemmed.csv")

        test = list(from_tsv_get(("data/test/" + fil + "Test_stemmed.csv",), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))



        other250 = sorted([(word[1][3] * math.log(float(len(lines))/sum(word[1][:2])), word[0]) for word in words.items()])[::-1][1800:]




        for other in other250:
            words[other[1]][2] = 0


        for line in test:

            sentiment = (line[1] == "Added" or line[2] == "1") and ( not line[1] == "Excluded" )



            rsv_sentiment = (calculateRsv(line[0], words, lins) > rsv_threshold) and isEnglish(line[0], words)



            if rsv_sentiment == sentiment:
                rsv += 1

            else:
                queries += ("Added    " if sentiment else "Excluded ") + "\t" + str(calculateRsv(line[0], words, lins)) + "\t" + sixty_char(line[0]) + str([words.get(word,[0,0,0])[2] for word in line[0].split()])  + "\n"

        with open("data/result/false.txt", "w") as false_fil:
                    false_fil.write(queries)



        print("%s     %s        %s"%( rsv, len(test) - rsv, len(test)))
    """
    #stem_file("data/train/firstTrain.csv")

    for i in range(1500):
        print prec_tfidf(i)

