# -*- coding:utf-8 -*-
from rsv import non_rel_hist, rel_hist, from_tsv_get
import itertools

def is_adjacent(lis, a, b):
    try:
        return lis.index(b) - lis.index(a) == 1
    except IndexError:
        return False


def get_prob_of_word(fil, word, rel=True):
    lines = from_tsv_get(fil, 'Search term', 'Added/Excluded', 'Conv. (1-per-click)')
    corpus1, corpus2 = itertools.tee(rel_hist(lines) if rel else non_rel_hist(lines), 2)
    total = sum(1 for element in corpus1)
    try:
        return sum(1 for sentence in corpus2 if word in sentence) / float(total)
    except ZeroDivisionError:
        return 0.0


def get_prob_of_words(fil, word1, word2, rel=True):
    lines = from_tsv_get(fil, 'Search term', 'Added/Excluded', 'Conv. (1-per-click)')
    corpus1, corpus2 = itertools.tee(rel_hist(lines) if rel else non_rel_hist(lines), 2)
    try:
        return sum(1 for sentence in corpus1 if is_adjacent(sentence, word1, word2)) / float(
            sum(1 for sentence in corpus2 if word1 in sentence))
    except ZeroDivisionError:
        return 0.0


def get_prob_of_query(fil, query, rel=True):
    words = query.split(" ")
    prob = get_prob_of_word(fil, words[0], rel)
    for index in xrange(1, len(words) - 1):
        prob *= get_prob_of_words(fil, words[index], words[index + 1], rel)
    return prob


if __name__ == "__main__":
    query = "social networks"
    print get_prob_of_query("data/data.tsv", query, True)
