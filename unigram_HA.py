"""
This one maintains a Spam Ham Unigram score for each hotels
and then tries to calculate the Confusion Matrix from that.
That is to mean, the training and test sets are confined in the hotel itself.
"""

from major import makeTrainingSet
import nltk

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

def analyseUsingUnigramScores(TestSet,SpamUnigramScores,HamUnigramScores):
    TestResult = []
    for entry in TestSet:
        entrySpamScore = 0
        entryHamScore  = 0
        UnigramList = GetUnigrams(entry[2])
        for unigram in UnigramList:
                entrySpamScore += SpamUnigramScores.get(unigram,1) #----FIND UNIGRAM SCORE IN SPAM
                entryHamScore += HamUnigramScores.get(unigram,1)   #----FIND UNIGRAM SCORE IN HAM
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

def getAccuracy(ConfusionMatrix):
    den = ConfusionMatrix[0][0] + ConfusionMatrix[1][1] + ConfusionMatrix[0][1] + ConfusionMatrix[1][0]
    if den == 0:
        return 0.0
    Accuracy = (ConfusionMatrix[0][0] + ConfusionMatrix[1][1])/(ConfusionMatrix[0][0] + ConfusionMatrix[1][1] + ConfusionMatrix[0][1] + ConfusionMatrix[1][0])
    return Accuracy
def main():
    TotalConfusion = [[0,0],[0,0]]
    maximumAcc = 0
    Hotels = ['affinia','allegro','amalfi','ambassador','conrad','fairmont','hardrock','hilton','homewood','hyatt','intercontinental','james','knickerbocker','monaco','omni','palmer','sheraton','sofitel','swissotel','talbott']

    for hotel in Hotels:
    #    print('-------MAKING TRAINING AND TEST SET------')
        TrainingSet, TestSet = makeTrainingSet(60)
    #    print('-------GETTING UNIGRAM SCORES------')
        SpamUnigramScores,HamUnigramScores = getUnigramScores(TrainingSet)
    #    print('-------GETTING REVIEW CLASSES------')
        TestClass = getReviewClass(TestSet)
    #    print('-------CALCULATING TEST RESULTS------')
        TestResults = analyseUsingUnigramScores(TestSet,SpamUnigramScores,HamUnigramScores)
    #    print('-------MAKING CONFUSION MATRIX------')
        ConfusionMatrix = makeConfusionMatrix(TestResults,TestClass)
        TotalConfusion[0][0] += ConfusionMatrix[0][0]
        TotalConfusion[0][1] += ConfusionMatrix[0][1]
        TotalConfusion[1][0] += ConfusionMatrix[1][0]
        TotalConfusion[1][1] += ConfusionMatrix[1][1]

        print(ConfusionMatrix)
        Accuracy = getAccuracy(ConfusionMatrix)
        maximumAcc = max(maximumAcc,Accuracy)
        print('Accuracy : ',Accuracy)
    print("--------------------------------------------------")
    print(TotalConfusion)
    Accuracy = getAccuracy(TotalConfusion)
    print('Accuracy : ',Accuracy)
    print('Maximum Accuracy : ',maximumAcc)


if __name__=="__main__":
    print('----ANALYSIS BEGINS----')
    main()
    print('----ANALYSIS ENDS----')
