#-------------------------------------------------------------------------------
# Name:        machinelearnPCA.py
# Purpose:	   Naive Bayes, SVM and Decision Tree classifiers along with Accuracy, confusion matrix, recall, precision and f1score calculations
#
# Author:      Smriti
#
# Created:     11/05/2015
# Copyright:   (c) Smriti 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from __future__ import division
from sklearn import tree,svm
from sklearn.naive_bayes import GaussianNB
import json

Pre = 0
Recall = 0
FScore =  0

def GetFeaturesFromFile(filename):
    f = open(filename,'r')
    p = json.load(f)
    return p

def TrainCT(TrainingFeatures,TrainingClass):
    clf = tree.DecisionTreeClassifier()
    clf.fit(TrainingFeatures,TrainingClass)
    return clf

def TestCT(clf,TestFeatures):
    results = clf.predict(TestFeatures)
    return results

def TrainNB(TrainingFeatures,TrainingClass):
    gnb = GaussianNB()
    y_pred = gnb.fit(TrainingFeatures,TrainingClass).predict(TrainingFeatures)
    return y_pred

def TestNB(y_pred,TestFeatures):
    results = y_pred.predict(TestFeatures)
    return results
    
def TrainSVM(TrainingFeatures,TrainingClass):
    clf = svm.SVC()
    clf.fit (TrainingFeatures,TrainingClass)
    return clf

def TestSVM(clf,TestFeatures):
    results = clf.predict(TestFeatures)
    return results


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
        
        Pre = CM[0][0]/(CM[0][0] + CM[1][0])
        try:
            Recall = CM[0][0]/(CM[0][0] + CM[0][1])
        except:
            Recall = 0
        try:
            FScore = 2 * ((Pre * Recall) / (Pre + Recall))        
        except:
            FScore = 0
    return CM, Pre, Recall, FScore



def main():
    TrainingFeatures = GetFeaturesFromFile('./machinelearn/TrainingFeatures')
    TrainingClass = GetFeaturesFromFile('./machinelearn/TrainingClass')
    TestFeatures = GetFeaturesFromFile('./machinelearn/TestFeatures')
    TestClass = GetFeaturesFromFile('./machinelearn/TestClass')
    print("RESULTS FROM CLASSIFICATION TREE")
    clf = TrainCT(TrainingFeatures,TrainingClass)
   # out_file = tree.export_graphviz(clf, out_file=tempfile.TemporaryFile())

    results = TestCT(clf,TestFeatures)
    cmatrix, Pre, Recall, FScore = makeConfusionMatrix(results,TestClass)
    Accuracy = (cmatrix[0][0] + cmatrix[1][1])/(cmatrix[0][0] + cmatrix[1][1]+0.0+(cmatrix[0][1] + cmatrix[1][0]))
    print(Accuracy)
    print(cmatrix)
    print(Pre)
    print(Recall)
    print(FScore)
    print("RESULTS FROM NAIVE BAYES")
    y_pred = TrainCT(TrainingFeatures,TrainingClass)
    results = TestCT(y_pred,TestFeatures)
    cmatrix, Pre, Recall, FScore = makeConfusionMatrix(results,TestClass)
    Accuracy = (cmatrix[0][0] + cmatrix[1][1])/(cmatrix[0][0] + cmatrix[1][1]+0.0+(cmatrix[0][1] + cmatrix[1][0]))
    print(Accuracy)
    print(cmatrix)
    print(Pre)
    print(Recall)
    print(FScore)
    print("RESULTS FROM SVM")
    clf = TrainSVM(TrainingFeatures,TrainingClass)
    results = TestSVM(clf,TestFeatures)
    cmatrix, Pre, Recall, FScore = makeConfusionMatrix(results,TestClass)
    Accuracy = (cmatrix[0][0] + cmatrix[1][1])/(cmatrix[0][0] + cmatrix[1][1]+0.0+(cmatrix[0][1] + cmatrix[1][0]))
    print(Accuracy)
    print(cmatrix)
    print(Pre)
    print(Recall)
    print(FScore)

if __name__=="__main__":

    main()
