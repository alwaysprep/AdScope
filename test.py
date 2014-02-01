#!/usr/bin/env python
# -*- coding:utf-8 -*-
from extract import from_tsv_get, hist, couple_hist, rel_non_rel_lines
from rsv import calculateRsv
from bigram import get_prob_of_query
from config import rsv_trashold

def extract_data(fil):
    lines = list(from_tsv_get((fil,), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))
    words = {}
    couples = {}
    hist(words, lines)
    couple_hist(couples, lines)
    lins = rel_non_rel_lines(lines)
    for word in words:
        words.get(word).append(calculateRsv(word, words, lins))

    return (words, couples, lins, lines)


def is_ok(a,b):
    return a >= b




if __name__ == "__main__":
    print("bigram\trsv\tbothTrue\tbothFalse\ttotal")


    fils = ["first", "second", "third", "fourth", "fifth", "sixth"]

    for fil in fils:
        rsv = 0
        bigram = 0
        when_same = 0
        both_false = 0
        queries = ""
        words, couples, lins, lines = extract_data("data/train/" + fil + "Train.csv")


        test = list(from_tsv_get(("data/test/" + fil + "Test.csv",), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))

        for line in test:

            sentiment = True if ((line[1] == "Added" or line[2] == "1") and ( not line[1] == "Excluded" )) else False

            bigram_sentiment = is_ok(get_prob_of_query(line[0], words, couples, True), get_prob_of_query(line[0], words, couples, False))

            rsv_sentiment = (calculateRsv(line[0], words, lins) > rsv_trashold)


            if bigram_sentiment == sentiment:
                bigram += 1

            if rsv_sentiment == sentiment:
                rsv += 1
                if rsv_sentiment == bigram_sentiment:
                    when_same += 1


            if (rsv_sentiment != sentiment)  and (rsv_sentiment == bigram_sentiment):
                both_false += 1
                queries +=  ("Added " if sentiment else "Excluded ") + str(calculateRsv(line[0], words, lins)) + " " + line[0]  + "\n"




        with open("data/result/false.txt", "w") as false_fil:
                    false_fil.write(queries)

        print("%s     %s    %s       %s         %s"%(bigram, rsv, when_same, both_false, len(test)))
        #print "For "+ fil +" test bigram: %s and rsv: %s same: %s both false: %s total query: %s" % (bigram, rsv, when_same, both_false, len(test))
