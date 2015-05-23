from sklearn import tree,svm
from StringIO import StringIO
#from sklearn.externals.six import StringIO
import json
import numpy as np
from sklearn.decomposition import PCA

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
    return CM



def analyse():
    TrainingFeatures =     GetFeaturesFromFile('./machinelearn/TrainingFeatures')
    TrainingClass = GetFeaturesFromFile('./machinelearn/TrainingClass')
    TestFeatures = GetFeaturesFromFile('./machinelearn/TestFeatures')
    TestClass = GetFeaturesFromFile('./machinelearn/TestClass')
    print("RESULTS FROM CLASSIFICATION TREE")
    clf = TrainCT(TrainingFeatures,TrainingClass)
    results = TestCT(clf,TestFeatures)
    cmatrix = makeConfusionMatrix(results,TestClass)
    Accuracy = (cmatrix[0][0] + cmatrix[1][1])/(cmatrix[0][0] + cmatrix[1][1]+0.0+(cmatrix[0][1] + cmatrix[1][0]))
    print(Accuracy)
    print(cmatrix)
    out = StringIO()
    out = tree.export_graphviz(clf, out_file=out)
    tree.export_graphviz(clf)
    print out.getvalue()
    graph_from_dot_data(out.getvalue()).write_pdf("somefile.pdf")

    print("RESULTS FROM SVM")
    clf = TrainSVM(TrainingFeatures,TrainingClass)
    results = TestSVM(clf,TestFeatures)
    cmatrix = makeConfusionMatrix(results,TestClass)
    Accuracy = (cmatrix[0][0] + cmatrix[1][1])/(cmatrix[0][0] + cmatrix[1][1]+0.0+(cmatrix[0][1] + cmatrix[1][0]))
    print(Accuracy)
    print(cmatrix)

def get_lineage(tree, feature_names):
     left      = tree.tree_.children_left
     right     = tree.tree_.children_right
     threshold = tree.tree_.threshold
     features  = [feature_names[i] for i in tree.tree_.feature]

     # get ids of child nodes
     idx = np.argwhere(left == -1)[:,0]

     def recurse(left, right, child, lineage=None):
          if lineage is None:
               lineage = [child]
          if child in left:
               parent = np.where(left == child)[0].item()
               split = 'l'
          else:
               parent = np.where(right == child)[0].item()
               split = 'r'

          lineage.append((parent, split, threshold[parent], features[parent]))

          if parent == 0:
               lineage.reverse()
               return lineage
          else:
               return recurse(left, right, parent, lineage)

     for child in idx:
          for node in recurse(left, right, child):
               print(node)

def analyseUsingPCA(K = 2):
    TrainingFeaturesOriginal =     GetFeaturesFromFile('./machinelearn/TrainingFeatures')
    TrainingClass = GetFeaturesFromFile('./machinelearn/TrainingClass')
    TestFeaturesOriginal = GetFeaturesFromFile('./machinelearn/TestFeatures')
    TestClass = GetFeaturesFromFile('./machinelearn/TestClass')

    TrainF = np.array(TrainingFeaturesOriginal)
    TestF = np.array(TestFeaturesOriginal)
    pca = PCA(n_components=2)

    TrainingFeatures = pca.fit_transform(TrainF)
    TestFeatures = pca.fit_transform(TestF)


    print("RESULTS FROM CLASSIFICATION TREE")
    clf = TrainCT(TrainingFeatures,TrainingClass)
    results = TestCT(clf,TestFeatures)
    cmatrix = makeConfusionMatrix(results,TestClass)
    Accuracy = (cmatrix[0][0] + cmatrix[1][1])/(cmatrix[0][0] + cmatrix[1][1]+0.0+(cmatrix[0][1] + cmatrix[1][0]))
    print(Accuracy)
    print(cmatrix)

    print("RESULTS FROM SVM")
    clf = TrainSVM(TrainingFeatures,TrainingClass)
    results = TestSVM(clf,TestFeatures)
    cmatrix = makeConfusionMatrix(results,TestClass)
    Accuracy = (cmatrix[0][0] + cmatrix[1][1])/(cmatrix[0][0] + cmatrix[1][1]+0.0+(cmatrix[0][1] + cmatrix[1][0]))
    print(Accuracy)
    print(cmatrix)


def main():
    analyseUsingPCA(K = 3)
if __name__=="__main__":
    main()
