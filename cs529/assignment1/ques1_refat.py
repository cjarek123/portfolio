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
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=X.shape[1])
        self.b_ = np.float64(0.)
        self.errors_ = []
        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_ += update * xi
                self.b_ += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self
    def net_input(self, X):
        return np.dot(X, self.w_) + self.b_
    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, 0)
s='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
df=pd.read_csv(s, header=None, encoding='utf-8')
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', 0, 1)
X = df.iloc[0:100, [0, 2]].values
ppn = Perceptron(eta=0.001, n_iter=10)
ppn.fit(X, y)
f=open("output.txt", 'w')
print('Perceptron Loss:',ppn.errors_, file=f)
print('Number of updates in Perceptron:',ppn.n_iter-ppn.errors_.count(0), file=f)
margin=abs(np.min((np.dot(X, ppn.w_)+ppn.b_)/np.linalg.norm(ppn.w_)))
print('Perceptron Margin:',margin, file=f)
print('For Perceptron converged in weight ',ppn.w_,' & bias ',ppn.b_, file=f)
class AdalineGD:
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
    def fit(self, X, y):
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=X.shape[1])
        self.b_ = np.float64(0.)
        self.losses_ = []
        for i in range(self.n_iter):
            net_input = self.net_input(X)
            output = self.activation(net_input)
            errors = (y - output)
            self.w_ += self.eta * 2.0 * X.T.dot(errors) / X.shape[0]
            self.b_ += self.eta * 2.0 * errors.mean()
            loss = (errors**2).mean()
            self.losses_.append(loss)
        return self
    def net_input(self, X):
        return np.dot(X, self.w_) + self.b_
    def activation(self, X):
        return X
    def predict(self, X):
        return np.where(self.activation(self.net_input(X))>= 0.5, 1, 0)
s='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
df=pd.read_csv(s, header=None, encoding='utf-8')
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', 0, 1)
X = df.iloc[0:100, [0, 2]].values
ppn = AdalineGD(eta=0.001, n_iter=10)
ppn.fit(X, y)
df = pd.DataFrame(ppn.losses_)
print('AdalineGD Loss:',df, file=f)
print('Number of updates in AdalineGD:',ppn.n_iter-ppn.losses_.count(0), file=f)
margin=abs(np.min((np.dot(X, ppn.w_)+ppn.b_)/np.linalg.norm(ppn.w_)))
print('AdalineGD Margin:',margin, file=f)
print('For AdalineGD converged in weight ',ppn.w_,' & bias ',ppn.b_, file=f)
f.close()
