import numpy as np
from sklearn.preprocessing import scale
from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt

def bench_k_means(estimator, name):
    estimator.fit(data)
    print('%-9s\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, estimator.inertia_,
             metrics.homogeneity_score(y, estimator.labels_),
             metrics.completeness_score(y, estimator.labels_),
             metrics.v_measure_score(y, estimator.labels_),
             metrics.adjusted_rand_score(y, estimator.labels_),
             metrics.adjusted_mutual_info_score(y, estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean')))

#classified if the picture in data is a picture of a digit using ddifrent scoring methods
if __name__ == '__main__':
    digits = load_digits()
    data = scale(digits.data)
    y = digits.target
    k = len(np.unique(y))
    samples, features = data.shape
    plt.matshow(data[0].reshape(8,8))
    plt.show()
    clf = KMeans(n_clusters=k, init="random", n_init=10)
    bench_k_means(clf, "1")
