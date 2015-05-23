from major import makeTrainingSet, saveToFile
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
from textblob import TextBlob

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

def GetFeatures(text, SpamBigramScores, HamBigramScores):

    HitsInSpamB, HitsInHamB = 0,0


    BigramList = GetBigrams(text)
    for Bigram in BigramList:
        if Bigram in SpamBigramScores.keys():
            HitsInSpamB += 1
        if Bigram in HamBigramScores.keys():
            HitsInHamB+= 1

    print    HitsInSpamB, HitsInHamB
    return [HitsInSpamB, HitsInHamB]

def makeFeatureVectors(TrainingSet, TestSet, SpamBigramScores, HamBigramScores):
    TrainingFeatures = []
    TrainingClass = []
    TestFeatures = []
    TestClass = []

    for entry in TrainingSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM

        #-------------------FEature Set---------------------------
        Features = []

        CalculatedFeatures = GetFeatures(entry[2],SpamBigramScores, HamBigramScores) #------------------------|--------OTHER CALCULATED METRIC
        for feature in CalculatedFeatures: Features.append(feature) #-------|

        Features.append(entry[3]) #------POLARITY

        #---------------------Class-------------------------------
        TrainingFeatures.append(Features)
        TrainingClass.append(entry[4])

    for entry in TestSet:
        #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
        #-------------------FEature Set---------------------------
        Features = []

        CalculatedFeatures = GetFeatures(entry[2], SpamBigramScores, HamBigramScores) #------------------------|--------OTHER CALCULATED METRIC
        for feature in CalculatedFeatures: Features.append(feature) #-------|

        Features.append(entry[3]) #------POLARITY

        #---------------------Class-------------------------------
        TestFeatures.append(Features)
        TestClass.append(entry[4])
    return TrainingFeatures,TrainingClass,TestFeatures,TestClass



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
    TrainingSet, TestSet = makeTrainingSet(80)
    print('-------GETTING UNIGRAM SCORES------')

    SpamBigramScores,HamBigramScores = getBigramScores(TrainingSet)

    print SpamBigramScores

    TrainingFeatures,TrainingClass,TestFeatures,TestClass = makeFeatureVectors(TrainingSet, TestSet, SpamBigramScores, HamBigramScores)

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

