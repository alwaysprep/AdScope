#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
from config import rsv_smoothing_factor, coefficient
from models import  Words

def calculateRsv(query, words):
    sentence = query.split(" ")
    total = 0
    for word in sentence:
        total += words.get(word, [0,0,0])[2]
    return total


def updatePtUt(w, temp_words):
    # 0 pos
    # 1 neg
    # 2 ab_pos
    # 3 ab_neg

    try:
        db_w = Words.objects.get(word = w)
    except Words.DoesNotExist:
        db_w = Words(
            word = w,
            pt=0,
            ut=0,
            c=0
        )
        db_w.save()
        db_w = Words.objects.get(word = w)



    alpha = rsv_smoothing_factor


    values = temp_words[w]

    pt = (values[0] + alpha + (coefficient * db_w.pt)) / (values[2] + coefficient + alpha)

    ut = (values[3] + alpha + (coefficient * db_w.ut)) / (values[1] + alpha + coefficient )

    db_w.pt = pt
    db_w.ut = ut
    db_w.c = math.log(pt) + math.log(ut)

    db_w.save()

