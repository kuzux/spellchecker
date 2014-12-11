from nltk.tokenize import RegexpTokenizer
from itertools import *
import sys

wordlist = None

def tokenize(text):
    tok = RegexpTokenizer("(\w+'\w+)|(\w+)")
    return map(lambda x: x.lower(), tok.tokenize(text))

def train(words):
    res = dict()
    for w in words:
        if w in res:
            res[w] += 1
        else:
            res[w] = 1
    return res

def make_dict(filename):
    res = None
    with open("corpus.txt") as f:
        res = train(tokenize(f.read()))
    
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

# words: an array of words
# return value: a set of words, which are both in the argument and the wordlist
def candidates(words):
    return set(ifilter(lambda w: w in wordlist, words))

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)

def corrected(word):
    if word in wordlist:
        return word

    neigh = neighbors(word)
    cands = candidates(neigh)

    if cands:
        return max(cands, key = wordlist.get)
    
    # cands2 is the set of words with an edit distance of 2
    cands2 = set(candidates(flatten(imap(lambda w: neighbors(w), neigh))))
    
    if cands2:
        return max(cands2, key = wordlist.get)

    # no replacement word found
    return ""

def main():
    if len(sys.argv) < 3:
        print "USAGE: spellchecker input output"
        return

    infile = sys.argv[1]
    outfile = sys.argv[2]
    global wordlist

    wordlist = make_dict()

    with open(infile, "r") as fin:
        with open(outfile, "w") as fout:
            for word in fin:
                fout.write(corrected(word.strip().lower()) + "\n")

if __name__ == '__main__':
    main()
