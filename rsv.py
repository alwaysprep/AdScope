#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
from config import rsv_smoothing_factor
def rsv(words, word, lins):
    rsv = {}
    rsv[word] = {
                  "positive": words.get(word, [0,0,0])[0],
                  "negative": words.get(word, [0,0,0])[1],
                  "absent_positive": lins[0] - words.get(word, [0,0,0])[0],
                  "absent_negative": lins[1] - words.get(word, [0,0,0])[1]
    }

    return rsv

def calculateC(word, words, lins):
    alpha = rsv_smoothing_factor
    table = rsv(words, word, lins)
    return math.log(((table[word]["positive"] + alpha ) / (table[word]["absent_positive"] + alpha)) / (
        ( table[word]["negative"] + alpha) / (table[word]["absent_negative"] + alpha)))


def calculateRsv(query, words, lins):
    sentence = query.split(" ")
    total = 0
    for word in sentence:
        total += calculateC(word, words, lins)
    return total


