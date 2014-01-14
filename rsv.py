# -*- coding:utf-8 -*-
from collections import defaultdict


def from_tsv_get(file_name, *args):
    lis = []
    with open(file_name) as tsv:
        tsv.readline() # first line is general info of file, it shouldn't be there
        columns = tsv.readline().split("\t") # second line column names
        columns[-1] = columns[-1].replace("\n", "")
        column_indexes = [columns.index(search_term) for search_term in args]

        for line in tsv:
            lis_line = line.split("\t")
            lis_line[-1] = lis_line[-1].replace("\n", "")
            lis.append([lis_line[col] for col in column_indexes])
    return lis


"""
def hist2(aFile):
	rel_words =[]
	non_rel_words = []
	lines = from_tsv_get(aFile, 'Search term', 'Added/Excluded', 'Conv. (1-per-click)')
	for line in lines:
		if (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded'):
			rel_words.extend(list(set(line[0])).split(" "))
		else:
			non_rel_words.extend(list(set(line[0])).split(" "))
	return len(rel_words), len(non_rel_words)

print hist2("araba.tsv")

def rsv2(query, aFile):

	rel_words, non_rel_words= hist(aFile)

	query = query.split()

	for word in query:
		rel_words.count(word)
		non_rel_words.count(word)
"""


def hist(afile):
    rel_words = []
    non_rel_words = []
    lines = from_tsv_get(afile, 'Search term', 'Added/Excluded', 'Conv. (1-per-click)')
    for line in lines:
        words = line[0].split()
        if (line[1] == 'Added' or line[2] == "1") and (not line[1] == 'Excluded'):
            rel_words.append(words)
        else:
            non_rel_words.append(words)
    return rel_words, non_rel_words


def rsv(query, afile):
    words = query.split()
    rel_words, non_rel_words = hist(afile)
    rel_dict = defaultdict(int)
    non_rel_dict = defaultdict(int)
    rsv = {}
    for word in words:
        for line in rel_words:
            if word in line:
                rel_dict[word] += 1

        for line in non_rel_words:
            if word in line:
                non_rel_dict[word] += 1

        rsv[word] = {
            "positive": rel_dict[word],
            "negative": non_rel_dict[word],
            "absent_positive": len(rel_words) - rel_dict[word],
            "absent_negative": len(non_rel_words) - non_rel_dict[word]
        }
    return rsv


if __name__ == "__main__":
    print rsv("what ning good", "data/data.tsv")