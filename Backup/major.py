#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Smriti
#
# Created:     12/05/2015
# Copyright:   (c) Smriti 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import random
import json
from DatabaseCreator import getHandle,clearHandle,DATABASE
import features
limit = ''
i = 0

#def main():
 #   pass




# debug mode

##def getFeatures(text):
##    return features.majorfunc("There is one handsome boy. The boy has now grown up. He is no longer a allegro now. He is good and in 100 hyatt or hilton.")

def getFeatures(text):
    return features.majorfunc(text)


def makeFeatureVectors(TrainingSet, TestSet):

    #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
    TrainingFeatures = []
    TestFeatures = []
    Features = []

    for entry in TrainingSet:
        CalculatedFeatures = getFeatures(entry[2]) # entry[2] has review text
        for feature in CalculatedFeatures: Features.append(feature)

        Features.append(entry[3]) #------POLARITY
        TrainingFeatures.append(Features)

    for entry in TestSet:
        CalculatedFeatures = getFeatures(entry[2]) # entry[2] has review text
        for feature in CalculatedFeatures: Features.append(feature)

        Features.append(entry[3]) #------POLARITY
        TestFeatures.append(Features)

    return TrainingFeatures, TestFeatures



# make TrainingSet[] and TestSet[]

##def makeTrainingSet(K):
##
##    TrainingSet = []
##    TestSet = []
##    conn = getHandle(DATABASE)
##
##    # Positive Spam
####    end = 40
##
##    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = 1 and SPAM = 1 "+limit+";"
##    cursor = conn.execute(query) # connect the database
##    data = cursor.fetchall() # fetch all queries
##    random.shuffle(data) # randomly shuffle all the data
##    length = len(data)
##    train = int((K * length) / 100) # number of queries fetched
##    temp = data[:train]
##    for entry in temp:
##        TrainingSet.append(entry) # append in TrainingSet[]
##    temp = data[train:]
##    for entry in temp:
##        TestSet.append(entry) # append in TestSet[]
##
##    # Positive Ham
##
##    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = 1 and SPAM = 0 "+limit+";"
##    cursor = conn.execute(query)
##    data = cursor.fetchall()
##    random.shuffle(data)
##    length = len(data)
##    train = int((K * length) / 100)
##    temp = data[:train]
##
##    for entry in temp: TrainingSet.append(entry)
##    temp = data[train:]
##    for entry in temp: TestSet.append(entry)
##
##    # Negative Spam
##
##    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = -1 and SPAM = 1 "+limit+";"
##    cursor = conn.execute(query)
##    data = cursor.fetchall()
##    random.shuffle(data)
##    length = len(data)
##    train = int((K * length) / 100)
##    temp = data[:train]
##    for entry in temp: TrainingSet.append(entry)
##    temp = data[train:]
##    for entry in temp: TestSet.append(entry)
##
##    # Negative Ham
##
##    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = -1 and SPAM = 0 "+limit+";"
##    cursor = conn.execute(query)
##    data = cursor.fetchall()
##    random.shuffle(data)
##    length = len(data)
##    train = int((K * length) / 100)
##    temp = data[:train]
##    for entry in temp: TrainingSet.append(entry)
##    temp = data[train:]
##    for entry in temp: TestSet.append(entry)
##
##    clearHandle(conn)
##    print(TestSet)
##    return TrainingSet, TestSet


def saveToFile(filename,content):
    f = open(filename,'w')
    json.dump(content,f)
    f.close()

# creating training and test data and saving features to files

def main():
    TrainingSet = []
    TestSet = []
    TrainingSet, TestSet = makeTrainingSet(70) #create the training and test files
# To make training and test data
##    print(TestSet)
##    saveToFile('./machinelearn/TrainingSet',TrainingSet)
##    saveToFile('./machinelearn/TestSet',TestSet)

    TrainingFeatures = []
    TestFeatures = []

##    TrainingReviewID,TestReviewID,TrainingFeatures,TrainingClass,TestFeatures,TestClass = makeFeatureVectors(TrainingSet, TestSet)
##
##    SaveFeaturesToFile('./machinelearn/TrainingFeatures',TrainingFeatures)
##    SaveFeaturesToFile('./machinelearn/TestFeatures',TestFeatures)
##    SaveFeaturesToFile('./machinelearn/TrainingClass',TrainingClass)
##    SaveFeaturesToFile('./machinelearn/TestClass',TestClass)


    getFeatures()

if __name__ == '__main__':
    print('This works')
    main()
    print('and stops')
