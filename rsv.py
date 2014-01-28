#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math

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
    table = rsv(words, word, lins)
    return math.log(((table[word]["positive"] + 0.5 ) / (table[word]["absent_positive"] + 0.5)) / (
        ( table[word]["negative"] + 0.5 ) / (table[word]["absent_negative"] + 0.5)))


def calculateRsv(query, words, lins):
    sentence = query.split(" ")
    total = 0
    for word in sentence:
        total += calculateC(word, words, lins)
    return total


