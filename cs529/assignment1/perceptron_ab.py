"""
Assignment One

CS529

Adrien Clay

Refat Mishuk

Christopher Jarek

Thomas Hynes
"""
import numpy as np
class PerceptronAbsorbedBias:
    """Perceptron classifier.
    
    Parameters
    ------------
    eta : float
      Learning rate (between 0.0 and 1.0)
    n_iter : int
      Passes over the training dataset.
    random_state : int
      Random number generator seed for random weight 
      initialization.
    
    Attributes
    -----------
    w_ : 1d-array
      Weights after fitting.
    b_ : Scalar
      Bias unit after fitting.
    errors_ : list
      Number of misclassifications (updates) in each epoch.
    
    """
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
    
    def fit(self, X, y):
        """Fit training data.
        Parameters
        ----------
        X : {array-like}, shape = [n_examples, n_features]
          Training vectors, where n_examples is the number of 
          examples and n_features is the number of features.
        y : array-like, shape = [n_examples]
          Target values.
        
        Returns
        -------
        self : object
        
        """
        # extend the weight vector to include the bias as the last element
        # this will result in the new shape
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01,
                              size=X.shape[1] + 1)
        
        # Add a 1 to the feature vector
        X_new = [np.append(x, 1) for x in X]

        self.errors_ = []
        
        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X_new, y):
                update = self.eta * (target - self.internal_predict_(xi))
                self.w_ += update * xi
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self
    
    def net_input(self, X):
        """Calculate net input"""
        return np.dot(X, self.w_)
    
    def internal_predict_(self, X):
        """
        Return class label after unit step
        Used internally as the input X will already be modified by fit
        """
        return np.where(self.net_input(X) >= 0.0, 1, 0)
    
    def predict(self, X):
        """
        Return class label after unit step

        Will be used for user input on .predict() call as X will need to be modified
        to be able to calculate net_input with augmented weight vector
        """
        X_new = [np.append(x, 1) for x in X]
        return np.where(self.net_input(X_new) >= 0.0, 1, 0)
