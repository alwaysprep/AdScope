#!/usr/bin/env python
# -*- coding:utf-8 -*-
from extract import from_tsv_get, hist, rel_non_rel_lines, totalNumOfWords
import math
from rsv import calculateRsv, calculateC, calculatePtUt, updatePtUt
from config import rsv_threshold, rsv_smoothing_factor
from nltk.corpus import wordnet
#import matplotlib.pyplot as plt
import pylab as pl
import numpy as np



def extract_data(fil, sf=None):
    lines = list(from_tsv_get((fil,), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))
    words = hist(lines)
    lins = rel_non_rel_lines(lines)


    for word in words:
        words[word] = list(calculatePtUt(word,words,lins))
        words.get(word).append(calculateC(word, words))

    return words


def update_words(lines, old_words, sf=None,):
    new_words = hist(lines)

    lins = rel_non_rel_lines(lines)
    for word in new_words:
        old_words[word] = list(updatePtUt(word,new_words, old_words,lins))
        old_words.get(word).append(calculateC(word, old_words))



def isEnglish(sentence, words):
    sentenceList = sentence.split()
    for word in sentenceList:
        if not wordnet.synsets(word) :
            if sum(words.get(word,[0,0])[:2]) < 3:
                return False
    return True

def sixty_char(sentence):
    return sentence + " " * (60 - len(sentence))



if __name__ == "__main__":

    files = ["first"] #, "second", "third", "fourth", "fifth", "sixth"]



    for fil in files:
        words = extract_data("data/train/" + fil + "Train.csv")


        test = list(from_tsv_get(("data/test/" + fil + "Test.csv",), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))

        new_train = []
        new_test = []


        for line in test:

            sentiment = (line[1] == "Added" or line[2] == "1") and ( not line[1] == "Excluded" )

            rsv_sentiment = (calculateRsv(line[0], words) > rsv_threshold) and isEnglish(line[0], words)

            if sentiment == rsv_sentiment:
                new_train.append(line)
            else:
                new_test.append(line)


        #print [(t[0], t[1], calculateRsv(t[0], words, lins)) for t in new_test]


        for iar in range(10):

            update_words(new_train, words)

            total = 0

            print len(new_test), "nt"

            for line in new_test:

                sentiment = (line[1] == "Added" or line[2] == "1") and (not line[1] == "Excluded" )

                rsv_sentiment = (calculateRsv(line[0], words) > rsv_threshold) and isEnglish(line[0], words)

                if sentiment == rsv_sentiment:
                    total += 1
            print(total)

        temp_test = new_test[:]
        new_test = []
        for line in temp_test:

            sentiment = (line[1] == "Added" or line[2] == "1") and ( not line[1] == "Excluded" )

            rsv_sentiment = (calculateRsv(line[0], words) > rsv_threshold) and isEnglish(line[0], words)

            if sentiment == rsv_sentiment:
                new_train.append(line)
            else:
                new_test.append(line)