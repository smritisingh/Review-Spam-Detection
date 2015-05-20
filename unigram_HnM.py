# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 23:09:01 2015

@author: Shaswat
@description:
This one will count on the basis of hit and miss
"""
from major import makeTrainingSet,saveToFile
import nltk

HOTELS = ['affinia','allegro','amalfi','ambassador','conrad','fairmont','hardrock','hilton','homewood','hyatt','intercontinental','james','knickerbocker','monaco','omni','palmer','sheraton','sofitel','swissotel','talbott']

def getReviewClass(GivenSet):
    ClassList = []
    for entry in GivenSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
        ClassList.append(entry[4])
    return ClassList

def GetUnigrams(text):
    text = text.lower()
    words = nltk.word_tokenize(text)
    return words

def getUnigramScores(TrainingSet):
    SpamUnigramScores = {}
    HamUnigramScores = {}
    for entry in TrainingSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM

        #---------------------Book Keeping------------------------
        #TrainingReviewID.append(entry[0])

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
    MissInSpam = 0
    MissInHam = 0
    UnigramList = GetUnigrams(text)
    for unigram in UnigramList:
        if unigram in SpamUnigramScores.keys():
            HitsInSpam += 1
        else:
            MissInSpam += 1
        if unigram in HamUnigramScores.keys():
            HitsInHam+= 1
        else:
            MissInHam += 1
    print    HitsInSpam, MissInSpam, HitsInHam, MissInHam
    return [HitsInSpam, MissInSpam, HitsInHam, MissInHam]

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
        Features.append(HOTELS.index(entry[1]))#------HOTEL NAME

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
        Features.append(HOTELS.index(entry[1]))#------HOTEL NAME

        #---------------------Class-------------------------------
        TestFeatures.append(Features)
        TestClass.append(entry[4])
    return TrainingFeatures,TrainingClass,TestFeatures,TestClass


def main():
    print('-------MAKING TRAINING AND TEST SET FOR INITIAL DATA------')
    TrainingSet, TestSet = makeTrainingSet(90)
    print('-------GETTING UNIGRAM SCORES------')
    SpamUnigramScores,HamUnigramScores = getUnigramScores(TrainingSet)

    TrainingFeatures,TrainingClass,TestFeatures,TestClass = makeFeatureVectors(TrainingSet, TestSet,SpamUnigramScores,HamUnigramScores)

    saveToFile('./machinelearn/TrainingFeatures',TrainingFeatures)
    saveToFile('./machinelearn/TestFeatures',TestFeatures)
    saveToFile('./machinelearn/TrainingClass',TrainingClass)
    saveToFile('./machinelearn/TestClass',TestClass)

if __name__=="__main__":
    print('----ANALYSIS BEGINS----')
    main()
    print('----ANALYSIS ENDS----')