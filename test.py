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


def rec(lis):

    new_train = []
    new_test = []

    for line in lis:

        sentiment = (line[1] == "Added" or line[2] == "1") and ( not line[1] == "Excluded" )

        rsv_sentiment = (calculateRsv(line[0], words) > rsv_threshold) and isEnglish(line[0], words)

        if sentiment == rsv_sentiment:
            new_train.append(line)
        else:
            new_test.append(line)

    return new_train, new_test


def print_prec(new_test, words):
    total=0
    for line in new_test:

        sentiment = (line[1] == "Added" or line[2] == "1") and (not line[1] == "Excluded" )

        rsv_sentiment = (calculateRsv(line[0], words) > rsv_threshold) and isEnglish(line[0], words)

        if sentiment == rsv_sentiment:
            total += 1
    print(total)


if __name__ == "__main__":

    fil = "first"

    words = extract_data("data/train/" + fil + "Train.csv")

    test = list(from_tsv_get(("data/test/" + fil + "Test.csv",), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))

    print_prec(test, words)

    new_train, new_test = rec(test)

    print new_train


    for ijk in range(10):

        new_train, new_test = rec(test)
        print str(len(new_test)) + "  ",

        update_words(new_train, words)
        print_prec(new_test, words)

        test = new_test[:]
