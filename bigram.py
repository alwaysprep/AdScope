#!/usr/bin/env python
# -*- coding:utf-8 -*-
def is_adjacent(lis, a, b):
    try:
        return lis.index(b) - lis.index(a) == 1
    except:
        return False


def get_prob_of_word(word, words, relevant):
    total = words.get(word, [0,0,0])[0 if relevant else 1]
    if total == 0:
        return 0.0
    return words.get(word, [0,0,0])[0 if relevant else 1] / float(total)


def get_prob_of_words(word1, word2, couples, words, relevant):
    total = float(words.get(word1, [0,0,0])[0 if relevant else 1])
    if total == 0:
        return 0.0
    return couples.get((word1, word2), [0, 0])[0 if relevant else 1] / total


def get_prob_of_query(query, words, couples, relevant=True):
    query = query.split(" ")
    prob = get_prob_of_word(query[0], words, relevant)
    for index in xrange(0, len(query) - 1):
        prob *= get_prob_of_words(query[index], query[index + 1], couples, words, relevant)
    return prob
