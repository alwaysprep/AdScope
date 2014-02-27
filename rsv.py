#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
from config import rsv_smoothing_factor, coefficient

def rsv(words, word, lins):
    rsv = {}
    rsv[word] = {
                  "positive": words.get(word, [0,0])[0],
                  "negative": words.get(word, [0,0])[1],
                  "absent_positive": lins[0] - words.get(word, [0,0])[0],
                  "absent_negative": lins[1] - words.get(word, [0,0])[1]
    }

    return rsv

def calculatePtUt(word, words, lins, sf = None):
    alpha = sf or rsv_smoothing_factor
    table = rsv(words, word, lins)
    return ((table[word]["positive"] + alpha) / (table[word]["absent_positive"] + alpha)),\
           ((table[word]["absent_negative"] + alpha) / (table[word]["negative"] + alpha))

def calculateC(word, words):

    return math.log(words.get(word)[0]) + math.log(words.get(word)[1])



def calculateRsv(query, words):
    sentence = query.split(" ")
    total = 0
    for word in sentence:
        total += words.get(word, [0,0,0])[2]
    return total


def updatePtUt(word, words, old_words,lins, k=None):
    table = rsv(words, word, lins)
    k = k or coefficient
    alpha = rsv_smoothing_factor
    if word not in old_words:
        return ((table[word]["positive"] + alpha) / (table[word]["absent_positive"] + alpha + k)),\
           ((table[word]["absent_negative"] + alpha + k) / (table[word]["negative"] + alpha))

    return ((table[word]["positive"] + k*old_words[word][0]) / (table[word]["absent_positive"] + k)),\
           ((table[word]["absent_negative"] + k) / (table[word]["negative"] + k*old_words[word][1]))
