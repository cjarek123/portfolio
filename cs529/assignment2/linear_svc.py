"""
CS 529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import numpy as np
class LinearSVC:

    """
    LinearSVC Classifier

    params:

    eta: Learning Rate (Float)
    n_iter: Number of iterations to train
    random_state: Random state for random variables
    C: Regularization paramter
    l2_param: Regularization Rate
    """
    

    def __init__(self, eta: float = .0001, n_iter: int = 50, random_state: int = 1, C: float = .1, l2_param: int = .1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
        self.C = C
        self.l2_param = l2_param

    def fit(self, X, y):

        """
        X: {array-like}, shape = [n_samples, n_features]
        y: {array-like}, shape = [n_samples]
        """

        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=X.shape[1])
        self.b_ = np.float64(0.)
        self.losses_ = []
        for _ in range(self.n_iter):
            net_input = self.net_input(X)
            
            # Compute hinge loss based on information in slides
            # Li = max{0, 1 - y * net_input}
            Li = np.where(y * net_input >= 1, 0, 1 - y * net_input)
            N = len(y)
            # L2 = lambda/2n * sum(w^2)
            l2_norm = self.l2_param * (1/(2 * N)) * np.sum(self.w_**2)
            loss = (self.C / N) * np.sum(Li) + l2_norm

            for i in range(N):
                # For each misclassified sample, utilize the derivative of the cost function with respect to w
                # to update the sample
                if (1 - y[i] * self.net_input(X[i])) > 0:
                    self.w_ = self.w_ - self.eta * (-(y[i] * X[i])) # derivative of hinge loss (dl/dw from slides)
                    self.b_ = self.b_ - (self.eta * y[i]) # dl\db from slides

            self.losses_.append(loss)
        return self
    def net_input(self, X):
        """Calculate Net Input"""
        return np.dot(X, self.w_) - self.b_
    

    def predict(self, X):
        return np.where(self.net_input(X) >= 0, 1, -1)
