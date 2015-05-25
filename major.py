from __future__ import division
#-------------------------------------------------------------------------------
# Name:        major.py
# Purpose:	   to make training and test datasets and to make the final feature vector from feature.py and SentmentScorer.py
#
# Author:      Smriti
#
# Created:     12/05/2015
# Copyright:   (c) Smriti 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import random
import json
from DatabaseCreator import getHandle,clearHandle,DATABASE
import features
import SentimentScorer
limit = ''
i = 0

#def main():
 #   pass




# debug mode

##def getFeatures():
##    text = "I hate this hotel."
##    print SentimentScorer.senti(text)

def getFeatures(text):
    return features.majorfunc(text)

def getSentiment(text):
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    count = text.count('.')+ text.count ('!')+ text.count('?')
    avg = 0
    for sent in sentences:
        avg += SentimentScorer.senti(sent)
    return avg/(len(sentences))


def makeFeatureVectors(TrainingSet, TestSet):

    #REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM
    TrainingFeatures = []
    TestFeatures = []
    TrainingClass = []
    TestClass = []
    Features1 = []
    Features2 = []
    list1 = []

    for entry in TrainingSet:
        Features1 = getFeatures(entry[2]) # entry[2] has review text
        Features1.append(getSentiment(entry[2]))
        Features1.append(entry[3]) #------POLARITY
        TrainingFeatures.append(Features1)
        Features1 = []
        TrainingClass.append(entry[4])

    for entry in TestSet:
        Features2 = getFeatures(entry[2]) # entry[2] has review text
        Features2.append(getSentiment(entry[2]))
        Features2.append(entry[3]) #------POLARITY
        TestFeatures.append(Features2)
        Features2 = []
        TestClass.append(entry[4])

    return TrainingFeatures, TestFeatures, TrainingClass, TestClass

# small dataset
##
### make TrainingSet[] and TestSet[]
##
##def makeTrainingSet(K):
##
##    TrainingSet = []
##    TestSet = []
##    conn = getHandle(DATABASE)
##
##    # Positive Spam
##    end = 40
##
##    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = 1 and SPAM = 1 "+limit+";"
##    cursor = conn.execute(query) # connect the database
##    data = cursor.fetchall() # fetch all queries
##    random.shuffle(data) # randomly shuffle all the data
##    length = len(data)
##    train = int((K * length) / 1000) # number of queries fetched
##    temp = data[:train]
##    for entry in temp:
##        TrainingSet.append(entry) # append in TrainingSet[]
##    temp = data[train:end]
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
##    train = int((K * length) / 1000)
##    temp = data[:train]
##
##    for entry in temp: TrainingSet.append(entry)
##    temp = data[train:end]
##    for entry in temp: TestSet.append(entry)
##
##    # Negative Spam
##
##    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = -1 and SPAM = 1 "+limit+";"
##    cursor = conn.execute(query)
##    data = cursor.fetchall()
##    random.shuffle(data)
##    length = len(data)
##    train = int((K * length) / 1000)
##    temp = data[:train]
##    for entry in temp: TrainingSet.append(entry)
##    temp = data[train:end]
##    for entry in temp: TestSet.append(entry)
##
##    # Negative Ham
##
##    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = -1 and SPAM = 0 "+limit+";"
##    cursor = conn.execute(query)
##    data = cursor.fetchall()
##    random.shuffle(data)
##    length = len(data)
##    train = int((K * length) / 1000)
##    temp = data[:train]
##    for entry in temp: TrainingSet.append(entry)
##    temp = data[train:end]
##    for entry in temp: TestSet.append(entry)
##
##    clearHandle(conn)
##    print(TestSet)
##    return TrainingSet, TestSet

#large dataset

def makeTrainingSet(K):

    TrainingSet = []
    TestSet = []
    conn = getHandle(DATABASE)

    # Positive Spam

    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = 1 and SPAM = 1 "+limit+";"
    cursor = conn.execute(query) # connect the database
    data = cursor.fetchall() # fetch all queries
    random.shuffle(data) # randomly shuffle all the data
    length = len(data)
    train = int((K * length) / 100) # number of queries fetched
    temp = data[:train]
    for entry in temp:
        TrainingSet.append(entry) # append in TrainingSet[]
    temp = data[train:]
    for entry in temp:
        TestSet.append(entry) # append in TestSet[]

    # Positive Ham

    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = 1 and SPAM = 0 "+limit+";"
    cursor = conn.execute(query)
    data = cursor.fetchall()
    random.shuffle(data)
    length = len(data)
    train = int((K * length) / 100)
    temp = data[:train]

    for entry in temp: TrainingSet.append(entry)
    temp = data[train:]
    for entry in temp: TestSet.append(entry)

    # Negative Spam

    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = -1 and SPAM = 1 "+limit+";"
    cursor = conn.execute(query)
    data = cursor.fetchall()
    random.shuffle(data)
    length = len(data)
    train = int((K * length) / 100)
    temp = data[:train]
    for entry in temp: TrainingSet.append(entry)
    temp = data[train:]
    for entry in temp: TestSet.append(entry)

    # Negative Ham

    query = "select REVIEWID, HOTELNAME, REVIEWTEXT, POLARITY, SPAM from REVIEWS where POLARITY = -1 and SPAM = 0 "+limit+";"
    cursor = conn.execute(query)
    data = cursor.fetchall()
    random.shuffle(data)
    length = len(data)
    train = int((K * length) / 100)
    temp = data[:train]
    for entry in temp: TrainingSet.append(entry)
    temp = data[train:]
    for entry in temp: TestSet.append(entry)

    clearHandle(conn)
    print(TestSet)
    return TrainingSet, TestSet


def saveToFile(filename,content):
    f = open(filename,'w')
    json.dump(content,f)
    f.close()

# creating training and test data and saving features to files

def main():
    TrainingSet = []
    TestSet = []

# debug

##    TrainingSet = [[1889, "sheraton", "I walked into this beautiful hotel and knew that I would have a wonderful stay in Chicago. After walking around the city all day, I was always excited to relax in this cleanly and superbly comforting place. The service was friendly and I especially liked the location. What a Treat!\n", 1, 1], [1802, "hyatt", "The Hyatt Regency in Chicago was a wonderful experience for my husband and I as we traveled through the area on vacation. After checking in we simply relaxed in the beautiful atrium for a while before going to our room. To our delight the room was very clean, ultra-modern and furnished with sleek and comfortable furniture. What really impressed us about the room was how spacious it was and the stunning river front views. We were pressed for time to make dinner so decided the Bistro sounded like the best option and it turned out to be a great choice! The food was simply fabulous. After dinner we were able to try out the fitness center, which ended up making our gym at home seem inadequate. This was just what we needed as a restful base for our Chicago vacation and we will definitely stay here again.\n", 1, 1]]
##    TestSet = [[1597, "talbott", "We loved the Talbott. The location was fabulous...very close to the shopping. The hotel is smaller, but the rooms are very nice. They are very spacious and are able to be darkened to sleep well. Also, the beds are some of the most comfortable I have ever slept in. I might also add that our room at queen beds. The staff is all friendly and puts them themselves out for you. The hotel has a cute outdoor eating area on the sidewalk that has flowers, etc. It looks like a scene out of Europe. I would highly recommend the hotel. We were there with our daughters; ages 10 and 13. \n", 1, 0], [1535, "sheraton", "i stayed at this hotel for a week with my family this hotel is huge so clean has comfy beds foods great staff couldn,t of being any nicer. stayed here for thanksgiving it was fabulous second time in chicago and still want to go back again ... the hotel is within walkin distance to both state street and michicgan avenue.There,s taxis right outside the hotel and the concierge can also ring for mini buses if your travelling with a big crowd.there,s also a cinema 2 mins away opposite the hotel . Perfect Hotel for a great get away ... \n", 1, 0]]

    TrainingSet, TestSet = makeTrainingSet(90) #create the training and test files
# To make training and test data

    saveToFile('./machinelearn/TrainingSet',TrainingSet)
    saveToFile('./machinelearn/TestSet',TestSet)

    print"Training and Test sets created"

# To make feature files

    TrainingFeatures = []
    TestFeatures = []
    TrainingClass = []
    TestClass = []

    TrainingFeatures,TestFeatures, TrainingClass, TestClass = makeFeatureVectors(TrainingSet, TestSet)

    saveToFile('./machinelearn/TrainingFeatures',TrainingFeatures)
    saveToFile('./machinelearn/TestFeatures',TestFeatures)
    saveToFile('./machinelearn/TrainingClass',TrainingClass)
    saveToFile('./machinelearn/TestClass',TestClass)

    print"Training and Test features created"

##    getFeatures()

if __name__ == '__main__':
    print('This works')
    main()
    print('and stops')
