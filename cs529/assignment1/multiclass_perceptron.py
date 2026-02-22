"""
Assignment One

CS529

Adrien Clay

Refat Mishuk

Christopher Jarek

Thomas Hynes
"""
from perceptron_ab import PerceptronAbsorbedBias
from adaline_gd import AdalineGD
import numpy as np

class MulticlassPerceptron:
    """
    Combines n number of perceptron or adaline models where n is the number of classes present in the input y vector

    For each class, instantiate a model that acknowledges the target class as one and the rest as zero.

    In predicting, ask each model for a prediction and return the first found 1

    Parameters
    ------------
    eta : float
      Learning rate (between 0.0 and 1.0)
    n_iter : int
      Passes over the training dataset.
    random_state : int
      Random number generator seed for random weight 
      initialization.
    model: str
        User choice between perceptron and adaline models (just for fun, assignment calls for perceptron so this is the default)
    """
    def __init__(self, eta: float = .01, n_iter: int = 50, random_state: int = 1, model: str = 'perceptron'):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
        self.model = model
        self.errors_ = {}

    
    def fit(self, X, y):
        # Get total number of classes that should be encoded into integers already
        # eg. full iris dataset will return set(y) = {0,1,2}
        self.classes = set(y)
        self.model_grid = {}

        # Create a model for each of the target classes
        for target_class in self.classes:
            if self.model == 'perceptron':
                self.model_grid[target_class] = PerceptronAbsorbedBias(eta=self.eta, n_iter=self.n_iter, random_state=self.random_state)
            elif self.model == 'adaline':
                self.model_grid[target_class] = AdalineGD(eta=self.eta, n_iter=self.n_iter, random_state=self.random_state)

        # For each target class, generate a new_y array for it that replaces the target class with 1 and all others with 0
        for target_class in self.classes:
            # Set 1 to be the target class
            # eg. if setosa is 0, set setosa to be 1 and set all others to 0
            # this would make class [0] = 1, [1, 2] = 0
            # this will make it a binary classification again
            new_y = [1 if value == target_class else 0 for value in y]
            
            # Train the perceptron for this target class
            self.model_grid[target_class] = self.model_grid[target_class].fit(X, new_y)
            self.errors_[int(target_class)] = self.model_grid[target_class].errors_
    


    def predict(self, X):

        # For each perceptron trained on each class, give it the 
        # input X array and get predictions
        self.predictions = {}
        for target_class in self.classes:
            preds = self.model_grid[target_class].predict(X)
            self.predictions[target_class] = preds
       
        final_preds = []

        for i in range(len(X)):
            pred_value = None
            # for each value in the data, get the first instance of 1
            # found for each perceptron, this will be the predicted value
            for target_class in self.classes:
                if self.predictions[target_class][i] == 1:
                      final_preds.append(target_class)
                      pred_value = target_class
                      break
            # No perceptron output a 1 meaning all perceptrons guessed 0, so default to 1 I guess?
            # Not sure how to handle this
            if pred_value is None:
                final_preds.append(1)
        # return array as expected shape (same shape as y: (n_samples,) ) 
        return np.array(final_preds).reshape(-1)
        
        

    