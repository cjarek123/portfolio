
"""
make_classification

Assignment 2

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk

"""
import numpy as np
from sklearn.model_selection import train_test_split

def make_classification(d: int = 2, n: int = 100, u: int = 100, random_state: int = 42):
    # random seed for numpy
    np.random.seed(random_state)

    # instantiate a for use in the overall equation ax + b
    a = np.random.uniform(low=-u, high=u, size=d)

    data = []
    labels = []

    # generate n random data points of dimension d
    # for d = 2 this will look like [[1,2],[-1,4]....n]
    x_points = [np.random.uniform(-u, u, size=d) for _ in range(n)]

    # get the distance from hyperplane 
    # 
    for point in x_points:
        distance = np.dot(a, point) + 0 # implicit b = 0
        data.append(point)
        labels.append(1 if distance >= 0 else -1)
    data = np.array(data)
    X_train, X_test, y_train, y_test = train_test_split(data, labels, stratify=labels, test_size=.3, random_state=random_state)
    # returns training/testing arrays, but also returns full data/labels at the end for graphing or whatever else
    return X_train, X_test, y_train, y_test, data, labels