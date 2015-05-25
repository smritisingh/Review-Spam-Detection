#-------------------------------------------------------------------------------
# Name:        unigram.py
# Purpose:	   to get unigram score and add to the feature vector
#
# Author:      Smriti
#
# Created:     11/05/2015
# Copyright:   (c) Smriti 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from major import makeTrainingSet, saveToFile
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

def getReviewClass(GivenSet):
    ClassList = []
    for entry in GivenSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
        ClassList.append(entry[4])
    return ClassList

def GetUnigrams(text):
    words = nltk.word_tokenize(text)
    return words

def getUnigramScores(TrainingSet):
    SpamUnigramScores = {}
    HamUnigramScores = {}
    for entry in TrainingSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM


        #-------------------FEature Set---------------------------
        UnigramList = GetUnigrams(entry[2])
        if entry[4] == 1:  #-------SPAM--------
            for unigram in UnigramList:
                SpamUnigramScores.setdefault(unigram,0)
                SpamUnigramScores[unigram] += 1
        elif entry[4] == 0:  #-------HAM--------
            for unigram in UnigramList:
                HamUnigramScores.setdefault(unigram,0)
                HamUnigramScores[unigram] += 1
    return SpamUnigramScores,HamUnigramScores

def GetFeatures(text,SpamUnigramScores,HamUnigramScores):
    HitsInSpam = 0
    HitsInHam = 0

    UnigramList = GetUnigrams(text)
    for unigram in UnigramList:
        if unigram in SpamUnigramScores.keys():
            HitsInSpam += 1
        if unigram in HamUnigramScores.keys():
            HitsInHam+= 1
    print    HitsInSpam, HitsInHam
    return [HitsInSpam, HitsInHam]

def makeFeatureVectors(TrainingSet, TestSet,SpamUnigramScores,HamUnigramScores):
    TrainingFeatures = []
    TrainingClass = []
    TestFeatures = []
    TestClass = []

    for entry in TrainingSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM

        #-------------------FEature Set---------------------------
        Features = []

        CalculatedFeatures = GetFeatures(entry[2],SpamUnigramScores,HamUnigramScores) #------------------------|--------OTHER CALCULATED METRIC
        for feature in CalculatedFeatures: Features.append(feature) #-------|

        Features.append(entry[3]) #------POLARITY

        #---------------------Class-------------------------------
        TrainingFeatures.append(Features)
        TrainingClass.append(entry[4])

    for entry in TestSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
        #-------------------FEature Set---------------------------
        Features = []

        CalculatedFeatures = GetFeatures(entry[2],SpamUnigramScores,HamUnigramScores) #------------------------|--------OTHER CALCULATED METRIC
        for feature in CalculatedFeatures: Features.append(feature) #-------|

        Features.append(entry[3]) #------POLARITY

        #---------------------Class-------------------------------
        TestFeatures.append(Features)
        TestClass.append(entry[4])
    return TrainingFeatures,TrainingClass,TestFeatures,TestClass


def analyseUsingUnigramScores(TestSet,SpamUnigramScores,HamUnigramScores):
    TestResult = []
    for entry in TestSet:
        entrySpamScore = 0
        entryHamScore  = 0
        UnigramList = GetUnigrams(entry[2])
        for unigram in UnigramList:
                if unigram.lower() not in stop:
                #print unigram, SpamUnigramScores.get(unigram), HamUnigramScores.get(unigram)
                    entrySpamScore += SpamUnigramScores.get(unigram,1) #----FIND UNIGRAM SCORE IN SPAM
                    entryHamScore += HamUnigramScores.get(unigram,1)   #----FIND UNIGRAM SCORE IN HAM
        print(entrySpamScore,entryHamScore)
        if entryHamScore - entrySpamScore > 0:
            print('HAM FOUND')
            TestResult.append(0)  #-------FOUND HAM
        else:
            print('SPAM FOUND')
            TestResult.append(1)  #-------FOUND SPAM
    return TestResult

def makeConfusionMatrix(results, TestClass):
    CM = [[0,0],[0,0]]
    if len(results) == len(TestClass):
        i = 0
        while i < len(results):
            if results[i] == 0 and TestClass[i] == 0:
                CM[0][0]+=1
            if results[i] == 0 and TestClass[i] == 1:
                CM[0][1]+=1
            if results[i] == 1 and TestClass[i] == 0:
                CM[1][0]+=1
            if results[i] == 1 and TestClass[i] == 1:
                CM[1][1]+=1
            i+=1
    return CM


def main():
    print('-------MAKING TRAINING AND TEST SET------')
    TrainingSet, TestSet = makeTrainingSet(70)
    print('-------GETTING UNIGRAM SCORES------')
    SpamUnigramScores,HamUnigramScores = getUnigramScores(TrainingSet)
    print SpamUnigramScores

    TrainingFeatures,TrainingClass,TestFeatures,TestClass = makeFeatureVectors(TrainingSet, TestSet,SpamUnigramScores,HamUnigramScores)

    saveToFile('./machinelearn/TrainingSet',TrainingSet)
    saveToFile('./machinelearn/TestSet',TestSet)
    saveToFile('./machinelearn/TrainingFeatures',TrainingFeatures)
    saveToFile('./machinelearn/TestFeatures',TestFeatures)
    saveToFile('./machinelearn/TrainingClass',TrainingClass)
    saveToFile('./machinelearn/TestClass',TestClass)

if __name__=="__main__":
    print('----ANALYSIS BEGINS----')
    main()
    print('----ANALYSIS ENDS----')

