from sklearn import datasets
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from scipy.special import expit
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
class LinearSVC:
    def __init__(self, eta=0.01, n_iter=50, regularization_param=1.0, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.regularization_param=regularization_param
        self.random_state = random_state
        self.weights = None
        self.bias = None
    def fit(self, X, y):
        np.random.seed(self.random_state)
        n_samples, n_features = X.shape
        y = np.where(y <= 0, -1, 1)
        self.weights = np.zeros(n_features)
        self.bias = 0
        for _ in range(self.n_iter):
            for i, x_i in enumerate(X):
                condition = y[i] * (self.net_input(x_i)) >= 1
                if condition:
                    self.weights -= self.eta * (2 * self.regularization_param * self.weights)
                else:
                    self.weights -= self.eta * ((2 * self.regularization_param * self.weights) - y[i]*x_i)
                    self.bias -= self.eta * y[i]
        return self
    def net_input(self, X):
        return np.dot(X, self.weights) + self.bias
    def predict(self, X):
        return np.sign(self.net_input(X))
    def predict_proba(self, X):
        scores = self.net_input(X)
        probabilities = expit(scores)  # Sigmoid function to convert scores to probabilities
        return np.column_stack([1 - probabilities, probabilities])

    def get_params(self, deep=True):
        return {
            "eta": self.eta,
            "n_iter": self.n_iter,
            "regularization_param": self.regularization_param,
            "random_state": self.random_state
        }
    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self
multi_class_svc = OneVsRestClassifier(LinearSVC(n_iter=1000, regularization_param=1.0, random_state=1))
multi_class_svc.fit(X_train_std, y_train)
predictions = multi_class_svc.predict(X_test_std)
accuracy = np.mean(predictions == y_test)
print("Predictions:", predictions)
print("Accuracy:", accuracy)
svm = SVC(kernel='linear', C=1.0, random_state=1)
svm.fit(X_train_std, y_train)
sklearn_predictions = svm.predict(X_test_std)
sklearn_accuracy = np.mean(sklearn_predictions == y_test)
print("Scikit-learn SVM Accuracy:", sklearn_accuracy)
    