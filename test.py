#!/usr/bin/env python
# -*- coding:utf-8 -*-
from extract import from_tsv_get, hist, rel_non_rel_lines, get_tf
import math
from rsv import calculateRsv, calculateC
from config import rsv_threshold, rsv_smoothing_factor
from nltk.corpus import wordnet
#import matplotlib.pyplot as plt
import pylab as pl
from sklearn import datasets, linear_model
import numpy as np
from stemming import stem_file
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVR
from sklearn import svm

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



def vectorize(doc, most, most_set):
    train_feature = []
    for train in doc:
        train = train.split()
        temp = [0 for i in range(700)]
        for t in train:
            if t in most_set:
                index = np.where(most==t)[0][0]
                temp[index] = 1
        train_feature.append(temp)
    return train_feature


def getLabel(lines):
    labels = []
    for line in lines:

        sentiment = (line[1] == "Added" or line[2] == "1") and ( not line[1] == "Excluded" )
        labels.append(1 if sentiment else 0)

    return labels



if __name__ == "__main__":

    files = ["first"]#, "second", "third", "fourth", "fifth", "sixth"]

    for fil in files:
        words, lins, lines = extract_data("data/train/" + fil + "Train.csv")

        test = list(from_tsv_get(("data/test/" + fil + "Test.csv",), ",", 'Search term', 'Added/Excluded', 'Conv. (1-per-click)'))

        first50 = sorted([[word[1][3] * math.log(float(len(lines))/sum(word[1][:2])), word[0]] for word in words.items()])[::-1][:700]



        first50 = np.array(first50)[:,1]

        set50 = set(first50)

        train_doc = np.array(lines)[:,0]
        test_doc = np.array(test)[:,0]


        train_feature = vectorize(train_doc, first50, set50)
        test_feature = vectorize(test_doc, first50, set50)

        train_label = getLabel(lines)
        test_label = getLabel(test)

        regr = linear_model.LinearRegression()

        regr.fit(train_feature, train_label)

        print('Coefficients: \n', regr.coef_)
        print("Residual sum of squares: %.2f" % np.mean((regr.predict(test_feature) - test_label) ** 2))
        print('Variance score: %.2f' % regr.score(test_feature, test_label))

        clf = LogisticRegression().fit(train_feature, train_label)
        clf2 = LinearSVC().fit(train_feature, train_label)
        clf3 = svm.SVC(degree = 1).fit(train_feature,train_label)
        clf4 = svm.SVR().fit(train_feature,train_label)

        print sum(1 for i in (test_label == clf.predict(test_feature)) if i)
        print sum(1 for i in (test_label == clf2.predict(test_feature)) if i)
        print sum(1 for i in (test_label == clf3.predict(test_feature)) if i)
        print sum(1 for i in (test_label == clf4.predict(test_feature)) if i)