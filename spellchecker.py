from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
import os.path
import pickle

def tokenize(text):
    tok = RegexpTokenizer("(\w+'\w+)|(\w+)")
    return map(lambda x: x.lower(), tok.tokenize(text))

def train(words):
    res = defaultdict(lambda: 0)
    for w in words:
        res[w] += 1    
    return res

def load_dict(filename):
    return pickle.load(open(filename, "rb"))

def make_dict(filename):
    res = None
    with open("corpus.txt") as f:
        res = train(tokenize(f.read()))
    
    pickle.dump(dict(res), open("dict.p", "wb"))

    return res

wordlist = None

if os.path.isfile("dict.p"):
    wordlist = load_dict("dict.p")
else:
    wordlist = make_dict("dict.p")

print len(wordlist)
