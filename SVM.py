import sklearn
from sklearn import datasets
from sklearn import svm
from sklearn import metrics
import matplotlib.pyplot as plt

#classified if a picture is a picture of breast cancer
if __name__ == '__main__':
    cancer = datasets.load_breast_cancer()

    # print(cancer.feature_names)
    # print(cancer.target_names)

    x = cancer.data
    y = cancer.target
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2)
    plt.matshow(x[100].reshape(5, 6))
    plt.show()
    classes = cancer.target_names

    clf = svm.SVC(kernel="poly", C=1)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    acc = metrics.accuracy_score(y_test, y_pred)
    print(acc)
