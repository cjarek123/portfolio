from sklearn import datasets
import numpy as np
iris=datasets.load_iris()
X=iris.data[:,[2,3]]
y=iris.target
print('class labels:',np.unique(y))
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=1, stratify=y)
print('label counts in y', np.bincount(y))
print('label counts in y_train', np.bincount(y_train))
print('label counts in y_test', np.bincount(y_test))
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
sc.fit(X_train)
X_train_std= sc.transform(X_train)
X_test_std= sc.transform(X_test)
from sklearn.svm import SVC
class LinearSVC:
    def __init__(self, eta=0.01, n_iter=50, regularization_param=1.0, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.regularization_param=regularization_param
        self.random_state = random_state
        self.svm = SVC(kernel='linear', C=self.regularization_param, max_iter=self.n_iter, random_state=self.random_state)
    def fit(self, X, y):
        self.svm.fit(X, y)
    def predict(self, X):
        return self.svm.predict(X)
linear_svc = LinearSVC(n_iter=1000, regularization_param=1.0, random_state=1)
linear_svc.fit(X_train_std, y_train)

predictions = linear_svc.predict(X_test_std)
print("Predictions:", predictions)

accuracy = np.mean(predictions == y_test)
print("Accuracy:", accuracy)
    