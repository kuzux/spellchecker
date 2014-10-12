from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
import os.path
import pickle

def tokenize(text):
    tok = RegexpTokenizer("(\w+'\w+)|(\w+)")
    return map(lambda x: x.lower(), tok.tokenize(text))

def train(words):
    res = defaultdict(lambda: 1)
    for w in words:
        res[w] += 1    
    return res

def load_dict(filename):
    return pickle.load(open(filename, "rb"))

def make_dict(filename):
    res = None
    with open("corpus.txt") as f:
        res = dict(train(tokenize(f.read())))
    
    pickle.dump(res, open("dict.p", "wb"))

    return res

# returns all possible words with an edit distance of 1 (damerau-levenshtein distance)
def neighbors(word):
    res = []
    n = len(word)
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for i in range(n+1):
        # split the word at ith character
        pre, suf = word[:i], word[i:]

        # w[i] deleted
        if i < n:
            res.append(pre + suf[1:])

        # w[i] and w[i+1] transposed
        if i < n-1:
            res.append(pre + suf[1] + suf[0] + suf[2:])

        # w[i] replaced by another character
        if i < n:
            for letter in alphabet:
                res.append(pre+letter+suf[1:])

        # a character inserted before w[i]
        for letter in alphabet:
            res.append(pre+letter+suf)

    return set(res)

wordlist = None

if os.path.isfile("dict.p"):
    wordlist = load_dict("dict.p")
else:
    wordlist = make_dict("dict.p")

print len(wordlist)
