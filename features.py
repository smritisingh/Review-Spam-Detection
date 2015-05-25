from __future__ import division
#-------------------------------------------------------------------------------
# Name:        features.py
# Purpose:		linguistic and POS featurs calculations
#
# Author:      Smriti
#
# Created:     11/05/2015
# Copyright:   (c) Smriti 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

print('-'*50)

# imports ----------------------------------------------------------------------

import collections
import nltk
from collections import Counter


from nltk.corpus import brown
from nltk.tag import UnigramTagger
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

from collections import Counter

import string
import re
import nltk

##textf = "There is one handsome boy. The boy has now grown up. He is no longer a allegro now. He is good and hyatt."
#debug mode
def majorfunc(line):

    textf = line;
#initialisations ---------------------------------------------------------------
##def majorfunc(textf):

    numLines = 0
    numSentences = 0
    numWords = 0
    numChars = 0
    numPunc = 0
    numUniqueWords = 0
    numBrand = 0
    numDigits = 0
    numVB = 0
    numNN = 0
    numCC = 0
    numJJ = 0
    numIN = 0
    numDT = 0
    numRB = 0
    numPRP = 0
    numConnect = 0
    numImme = 0
    totNN, totJJ, totIN, totDT, totVB, totRB, totPRP, totCC = 0,0,0,0,0,0,0,0

    # arrays -----------------------------------------------------------------------

    brands = {'affinia', 'allegro', 'amalfi', 'ambassador', 'conrad', 'fairmont', 'hardrock', 'hilton', 'homewood', 'hyatt', 'intercontinental', 'james', 'knickerbocker', 'monaco', 'omni', 'palmer', 'sheraton', 'sofitel', 'swissotel', 'talbott'}
    Nouns = {'NN', 'NNS', 'NNP', 'NNPS'}
    Verbs = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
    Pronouns = {'IN'}
    Prepo = {'PRP', 'PRP$'}
    Conjuncs = {'CC', 'IN'}
    Puncs = {'.','?','!', ',','"','<','>','/','{','}','[',']','|','(',')','@','#','$','%','^','&','*','(',')','-','_','+','=','~','`',':',';'}
    Imme = {'me', 'mine', 'us', 'our', 'ours', 'I', 'mine', 'we'}
    Connect = {'and', 'or', 'else', 'whether', 'eventually', 'however', 'furthermore', 'also', 'subsequently', 'consequently', 'evidently', 'whoever', 'whichever'}
    Adj = {'JJ', 'JJR', 'JJS'}
    Adverbs = {'RB', 'RBR', 'RBS'}
    Deter = {'DT'}

    #def printLine(ln):
        #print ln

    # functions --------------------------------------------------------------------

    def calcImme(text):
        cnt = 0
        for j in text:
            if(j in Imme):
                cnt += 1
##        print cnt
        return cnt

    def calcConnect(text):
        cnt = 0
        for j in text:
            if(j in Connect):
                cnt += 1
##        print cnt
        return cnt

    def tokenizeLine(ln):
        tempwords = nltk.word_tokenize(ln)
        return tempwords

    def calcLetters(ln):
        return len(ln) - ln.count(' ')

    def calcDigits(ln):
        return len([c for c in ln if c.isdigit()])

    def calcPunc(text):
        cnt = 0
        for j in text:
##            print j
            if(j in Puncs):
                cnt += 1
        return cnt

    def calcBrand(text):
        cnt = 0
        for j in text:
##            print j
            if(j in brands):
                cnt += 1
        return cnt

    def calcUniqueWords(ln):
        return len(set(re.findall('\w+', ln.lower())))

    def calcPOS(ln):
        POStag = pos_tag(word_tokenize(ln))
        c = Counter([j for i,j in POStag])

        numNN, numJJ, numIN, numDT, numVB, numRB, numPRP, numCC = 0, 0, 0, 0, 0, 0, 0, 0
        for j in c.keys():
            if (j in Nouns):
                numNN += c.get(j)
            if (j in Adj):
                numJJ += c.get(j)
            if (j in Prepo):
                numIN += c.get(j)
            if (j in Deter):
                numDT += c.get(j)
            if (j in Verbs):
                numVB += c.get(j)
            if (j in Adverbs):
                numRB += c.get(j)
            if (j in Pronouns):
                numPRP += c.get(j)
            if (j in Conjuncs):
                numCC += c.get(j)

        return numNN, numJJ, numIN, numDT, numVB, numRB, numPRP, numCC


    def calcARI(numChars, numWords, numSentences):
##        print numChars, numWords, numSentences
##        print ((4.71 * (numChars/numWords)) + (0.5 * (numWords/numSentences)) - 21.43)
        return ((4.71 * (numChars+1/numWords+1)) + (0.5 * (numWords+1/numSentences+1)) - 21.43)


    # main program -----------------------------------------------------------------

##    print line
    tokenSent = tokenizeLine(line) # tokenized sentence
##    print tokenSent
    numLines += 1
    numSentences += line.count('.')+ line.count ('!')+ line.count('?') # total num of sentences
    numWords +=  len(tokenSent) # total num of words

    numChars = calcLetters(line)
    numDigits = calcDigits(line)
    numPunc = calcPunc(tokenSent)

    numBrand = calcBrand(tokenSent)
    numImme = calcImme(tokenSent)
    numConnect = calcConnect(tokenSent)
    numUniqueWords = calcUniqueWords(line)

    totNN, totJJ, totIN, totDT, totVB, totRB, totPRP, totCC = 0,0,0,0,0,0,0,0

    totNN, totJJ, totIN, totDT, totVB, totRB, totPRP, totCC = calcPOS(line) # calculate POS tags for each token

    #ARI = calcARI((numChars - numPunc), (numWords - numPunc), numSentences)

    # results ----------------------------------------------------------------------
##    print numChars
##    print numWords
##    print numSentences
##    print 'Quantity :'
##    print numWords - totPunc
##    print 'Complexity :'
##    print ARI
##    print 'Diversity :'
##    print totUniqueWords
##    print 'Immediacy :'
##    print numPP/numWords
##    print 'Branding :'
##    print totBrand
##    print 'Average Word Length :'
##    print totChars/numWords
##    print 'Number of Connectors :'
##    print numCC
##    print 'Number of Digits :'
##    print totDigits
##    print 'Ratio of VB to NN :'
##    print (numVB + 1) /(numNN + 1)

##    return [(numWords - numPunc),(((numWords - numPunc)+1)/(numSentences+1)), numUniqueWords, ((numImme +1)/(numWords+1)), numBrand, ((numChars+1)/(numWords+1)), numConnect, numDigits,((numVB + 1) /(numNN + 1))]
# Linguistic Characteristics: Quantity, Complexity, Diversity, Branding, Avg Word Length, Digits
##    return [(numWords - numPunc),(((numWords - numPunc)+1)/(numSentences+1)), numUniqueWords,  numBrand, ((numChars+1)/(numWords+1)),  numDigits ]
# POS Features: NN, JJ, IN, DT, VB, RB, PRP (Immediacy), CC(Conjunctions)
##    return [totNN, totJJ, totIN, totDT, totVB, totRB, (totPRP + numConnect), (totCC + numImme) ]
# Both Features:
##    return [(numWords - numPunc),(((numWords - numPunc)+1)/(numSentences+1)), numUniqueWords,  numBrand, ((numChars+1)/(numWords+1)),  numDigits ,totNN, totJJ, totIN, totDT, totVB, totRB, (totPRP + numConnect), (totCC + numImme)]
    return [(numWords - numPunc),(((numWords - numPunc)+1)/(numSentences+1)), numUniqueWords, ((numImme +1)/(numWords+1)), numBrand, ((numChars+1)/(numWords+1)), numConnect, numDigits,((numVB + 1) /(numNN + 1))]


##    print ((numWords - totPunc), ARI, totUniqueWords, (numPP/numWords), totBrand, (totChars/numWords), numCC, totDigits,((numVB + 1) /(numNN + 1)))
##    return ((numWords - totPunc), ARI, totUniqueWords, (numPP/numWords), totBrand, (totChars/numWords), numCC, totDigits,((numVB + 1) /(numNN + 1)))
##    textf.close()
    #-------------------------------------------------------------------------------
