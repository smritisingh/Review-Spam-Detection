

from textblob import TextBlob
from major import makeTrainingSet
import nltk

#import machinelearn

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

def analyseUsingBigramScores(TestSet,SpamBigramScores,HamBigramScores):
    TestResult = []
    for entry in TestSet:
        entrySpamScore = 0
        entryHamScore  = 0
        BigramList = GetBigrams(entry[2])
        for Bigram in BigramList:
                entrySpamScore += SpamBigramScores.get(Bigram,1) #----FIND Bigram SCORE IN SPAM
                entryHamScore += HamBigramScores.get(Bigram,1)   #----FIND Bigram SCORE IN HAM
        #print(entrySpamScore,entryHamScore)
        if entryHamScore - entrySpamScore > 0:
            #print('HAM FOUND')
            TestResult.append(0)  #-------FOUND HAM
        else:
            #print('SPAM FOUND')
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
    print('-------GETTING Bigram SCORES------')
    SpamBigramScores,HamBigramScores = getBigramScores(TrainingSet)
    print('-------GETTING REVIEW CLASSES------')
    TestClass = getReviewClass(TestSet)
    print('-------CALCULATING TEST RESULTS------')
    TestResults = analyseUsingBigramScores(TestSet,SpamBigramScores,HamBigramScores)
    print('-------MAKING CONFUSION MATRIX------')
    ConfusionMatrix = makeConfusionMatrix(TestResults,TestClass)
    print(ConfusionMatrix)
    Accuracy = (ConfusionMatrix[0][0] + ConfusionMatrix[1][1])/(ConfusionMatrix[0][0] + ConfusionMatrix[1][1] + ConfusionMatrix[0][1] + ConfusionMatrix[1][0] + 0.0)
    print('Accuracy : ',Accuracy)

if __name__=="__main__":
    print('----ANALYSIS BEGINS----')
    main()
    print('----ANALYSIS ENDS----')
    #machinelearn.main()