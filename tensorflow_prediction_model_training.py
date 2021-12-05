import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style

def bestScore(x,y):
    best = 0
    list1=list()
    for _ in range(100):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

        linear = linear_model.LinearRegression()
        linear.fit(x_train, y_train)
        acc = linear.score(x_test, y_test)

        if acc > best:
            best = acc
            list1.append(acc)
            with open("resource/tensorflow_prediction_model_training/studentmodel.pickle", "wb") as f:
                pickle.dump(linear, f)
    return sum(list1)/len(list1)

def main():
    data = pd.read_csv("resource/tensorflow_prediction_model_training/student-mat.csv", sep=";")
    data = shuffle(data[["G1", "G2", "G3", "studytime", "failures", "absences"]])
    predict = "G3"
    x = np.array(data.drop([predict], 1))
    y = np.array(data[predict])
    for i in np.arange(0.01,0.4,0.01):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
        '''bestScore(x, y,)'''

    pickle_in = open("resource/tensorflow_prediction_model_training/studentmodel.pickle", "rb")
    linear = pickle.load(pickle_in)

    print("Score: \n",linear.score(x_test, y_test))
    print('Coefficient: \n', linear.coef_)  # These are each slope value
    print('Intercept: \n', linear.intercept_)
    predictions = linear.predict(x_test)

    print(x_test)

    p = "G2"
    style.use("ggplot")
    pyplot.scatter(data[p], data[predict])
    pyplot.xlabel(p)
    pyplot.ylabel(predict)
    pyplot.show()

if __name__ == '__main__':
    main()