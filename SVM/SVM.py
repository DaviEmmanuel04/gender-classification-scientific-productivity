try:
    import numpy as np
    import pandas as pd
    from sklearn import svm
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import train_test_split
    from nltk import classify
    from nltk.classify.scikitlearn import SklearnClassifier
except Exception as e:
    print(e)

_mount = False

try:
    from google.colab import drive
    drive.mount('/content/drive')
    _mount = True
except:
    print("Failed to mount with drive.")

class SVM:
    def __init__(self):
        self.data = None
        self.clf = None
        self.acc = None

    def classify(self, value):
        if type(value) == str:
            return self.clf.classify(self.prepareData(value,op=2))
        else:
            return self.clf.classify_many(self.prepareData(value, op=1))   

    def prepareData(self, names, genders=0, op=0):
        if type(genders) == int:
            genders = [0]*len(names)
        dataSet = list()
        for name, gender in zip(names, genders):
            name = name.lower()
            dictName = {'name':name,
                        'firstChar':name[0],
                        'lastChar':name[-1],
                        'lastTwoChar':name[-2:],
                        'lastThreeChar':name[-3:],
                        'length':len(name)
                        }
            if op == 0:
                dataSet.append((dictName, gender))
            if op == 1:
                dataSet.append(dictName)
            if op == 2:
                return dictName

        return dataSet

    def training(self, typeSVM="linearsvc", test_size=0.2, random_state=28):
        if _mount:
            dfData = pd.read_csv("drive/MyDrive/Colab Notebooks/grupos.csv")
        else:
            try:
                dfData = pd.read_csv(r"SVM/grupos.csv")
            except:
                raise Exception("Impossible to do training. Database not found.")
        
        names = dfData["name"].apply(lambda x: x.lower())
        classification = dfData['classification']

        self.data = self.prepareData(names, classification)

        treino, teste = train_test_split(self.data, test_size=test_size, random_state=random_state)

        if typeSVM.lower() == "linear":
            self.clf = SklearnClassifier(svm.SVC(kernel="linear", C=10.0))
        elif typeSVM.lower() == "linearsvc":
            self.clf = SklearnClassifier(svm.LinearSVC(C=1.0, max_iter=1000000))
        elif typeSVM.lower() == "rbf":
            self.clf = SklearnClassifier(svm.SVC(kernel="rbf", gamma=0.01, C=100.0))
        elif typeSVM.lower() == "nurbf":
            self.clf = SklearnClassifier(svm.NuSVC(kernel="rbf", gamma=0.01, nu=0.1))
        elif typeSVM.lower() == "poly":
            self.clf = SklearnClassifier(svm.SVC(kernel='poly', gamma='auto', degree=1, C=100.0))
        elif typeSVM.lower() == "nupoly":
            self.clf = SklearnClassifier(svm.NuSVC(kernel='poly', gamma='auto', degree=1, nu=0.3))
        elif typeSVM.lower() == "sigmoid":
            self.clf = SklearnClassifier(svm.SVC(kernel='sigmoid', gamma=0.01, C=0.01))
        elif typeSVM.lower() == "sigmoid":
            self.clf = SklearnClassifier(svm.NuSVC(kernel='sigmoid', gamma=0.01, nu=0.9))
        else:
            raise Exception("SVM model not available.")

        self.clf = self.clf.train(treino)
        self.acc = classify.accuracy(self.clf, teste)

if __name__ == "__main__":
    svc = SVM()
    svc.training(typeSVM = "linearsvc")
    print(svc.acc)
    print(svc.classify(["Gabriel", "Milena", "Walkir"]))