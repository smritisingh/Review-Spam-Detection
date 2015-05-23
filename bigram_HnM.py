# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 23:09:01 2015

@author: Shaswat
@description:
This one will count on the basis of hit and miss for bigrams
"""
from mainFile import makeTrainingSet,SaveFeaturesToFile
import nltk
#import machinelearn
from textblob import TextBlob

HOTELS = ['affinia','allegro','amalfi','ambassador','conrad','fairmont','hardrock','hilton','homewood','hyatt','intercontinental','james','knickerbocker','monaco','omni','palmer','sheraton','sofitel','swissotel','talbott']

def getReviewClass(GivenSet):
    ClassList = []
    for entry in GivenSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
        ClassList.append(entry[4])
    return ClassList

def GetBigrams(text):
    blob = TextBlob(text)
    WordLists = blob.ngrams(n = 2)
    Bigrams = []
    for wordlist in WordLists:
       cstr = ''
       for word in wordlist:    cstr = cstr+word+"_"
       Bigrams.append(cstr)
    return Bigrams

def getBigramScores(TrainingSet):
    SpamBigramScores = {}
    HamBigramScores = {}
    for entry in TrainingSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
        
        #---------------------Book Keeping------------------------
        #TrainingReviewID.append(entry[0])
        
        #-------------------FEature Set---------------------------
        BigramList = GetBigrams(entry[2])
        if entry[4] == 1:  #-------SPAM--------
            for Bigram in BigramList:
                SpamBigramScores.setdefault(Bigram,0)
                SpamBigramScores[Bigram] += 1
        elif entry[4] == 0:  #-------HAM--------
            for Bigram in BigramList:
                HamBigramScores.setdefault(Bigram,0)
                HamBigramScores[Bigram] += 1
    return SpamBigramScores,HamBigramScores

def GetFeatures(text,SpamBigramScores,HamBigramScores):
    HitsInSpam = 0
    HitsInHam = 0
    MissInSpam = 0
    MissInHam = 0
    BigramList = GetBigrams(text)
    for Bigram in BigramList:
        if Bigram in SpamBigramScores.keys():
            HitsInSpam += 1
        else:
            MissInSpam += 1
        if Bigram in HamBigramScores.keys():
            HitsInHam+= 1
        else:
            MissInHam += 1
    return [HitsInSpam, MissInSpam, HitsInHam, MissInHam]
    
def makeFeatureVectors(TrainingSet, TestSet,SpamBigramScores,HamBigramScores):
    TrainingFeatures = []
    TrainingClass = []
    TestFeatures = []
    TestClass = []

    for entry in TrainingSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
        
        #-------------------FEature Set---------------------------
        Features = []
        
        CalculatedFeatures = GetFeatures(entry[2],SpamBigramScores,HamBigramScores) #------------------------|--------OTHER CALCULATED METRIC
        for feature in CalculatedFeatures: Features.append(feature) #-------|
        
        Features.append(entry[3]) #------POLARITY
        Features.append(HOTELS.index(entry[1]))
        
        #---------------------Class-------------------------------
        TrainingFeatures.append(Features)
        TrainingClass.append(entry[4])

    for entry in TestSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
        #-------------------FEature Set---------------------------
        Features = []
        
        CalculatedFeatures = GetFeatures(entry[2],SpamBigramScores,HamBigramScores) #------------------------|--------OTHER CALCULATED METRIC
        for feature in CalculatedFeatures: Features.append(feature) #-------|

        Features.append(entry[3]) #------POLARITY
        Features.append(HOTELS.index(entry[1]))

        #---------------------Class-------------------------------
        TestFeatures.append(Features)
        TestClass.append(entry[4])
    return TrainingFeatures,TrainingClass,TestFeatures,TestClass


def main():
    print('-------MAKING TRAINING AND TEST SET FOR INITIAL DATA------')
    TrainingSet, TestSet = makeTrainingSet(90)
    print('-------GETTING Bigram SCORES------')
    SpamBigramScores,HamBigramScores = getBigramScores(TrainingSet)
    print('-------MAKING TRAINING AND TEST SET ------')
    
    TrainingSet, TestSet = makeTrainingSet(90)
    TrainingFeatures,TrainingClass,TestFeatures,TestClass = makeFeatureVectors(TrainingSet, TestSet,SpamBigramScores,HamBigramScores)
    
    SaveFeaturesToFile('./machinelearn/TrainingFeatures',TrainingFeatures)
    SaveFeaturesToFile('./machinelearn/TestFeatures',TestFeatures)
    SaveFeaturesToFile('./machinelearn/TrainingClass',TrainingClass)
    SaveFeaturesToFile('./machinelearn/TestClass',TestClass)

if __name__=="__main__":
    print('----ANALYSIS BEGINS----')
    main()
    print('----ANALYSIS ENDS----')
    #machinelearn.main()