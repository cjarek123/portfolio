import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
class Perceptron:
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
    def fit(self, X, y):
        X_bias = np.c_[np.ones(X.shape[0]), X]
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=X_bias.shape[1])
        self.errors_ = []
        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X_bias, y):
                update = self.eta * (target - self.predict(xi))
                self.w_ += update * xi
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self
    def net_input(self, X):
        return np.dot(X, self.w_) 
    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, 0)
s='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
df=pd.read_csv(s, header=None, encoding='utf-8')
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', 0, 1)
X = df.iloc[0:100, [0, 2]].values
X_bias = np.c_[np.ones(X.shape[0]), X]
ppn = Perceptron(eta=0.001, n_iter=10)
ppn.fit(X, y)
f=open("output2.txt", 'w')
print('Perceptron Loss:',ppn.errors_, file=f)
print('Number of updates in Perceptron:',ppn.n_iter-ppn.errors_.count(0), file=f)
margin=abs(np.min((np.dot(X_bias, ppn.w_))/np.linalg.norm(ppn.w_)))
print('Perceptron Margin:',margin, file=f)
print('For Perceptron converged in weight ',ppn.w_, file=f)
f.close()
