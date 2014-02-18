from nltk.stem import PorterStemmer
st=PorterStemmer() # better performance from Lancaster

def stem_file(fil):
    w = open(fil.replace(".csv", "") + "_stemmed.csv" , "w")

    with open(fil) as docs:
        w.write(docs.readline())
        for doc in docs:
            line = doc.split(",")
            line[0] = " ".join([st.stem(word) for word in  line[0].split()])

            w.write(",".join(line))

