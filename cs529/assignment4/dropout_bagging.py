"""
CS529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import torch
from FNNWithDropout import FNNWithDropout
from torch.utils.data import DataLoader, RandomSampler, Dataset
import numpy as np
import warnings
import sys
import time
warnings.filterwarnings('ignore', category=UserWarning)



class DropoutBagging:


    def __init__(self, num_models = 3, learning_rate = 0.0001, weight_decay = 0, dropout_prob = .3):
        self.num_models = num_models
        self.models: list[FNNWithDropout] = []
        self.scores = []
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.dropout_prob = dropout_prob
        self.train_time = 0


    def train_model(self, train_data: DataLoader, test_data: DataLoader, init_shape: int, epochs, verbose):
        model = FNNWithDropout(init_shape=init_shape, learning_rate=self.learning_rate, weight_decay=self.weight_decay, dropout_prob=self.dropout_prob)

        model.fit(train_data, verbose=verbose, epochs=epochs)

        test_accuracy = model.evaluate(test_data)
        return model, test_accuracy

    def predict(self, X: torch.Tensor):
        output = [model.predict_proba(X).detach().numpy() for model in self.models]
        preds = np.array(output)
        summed_preds = np.sum(preds, axis=0)
        result = np.argmax(summed_preds, axis=1)
        return result


    def fit(self, train_dataset: Dataset, test_dataset: Dataset, init_shape: int, epochs = 10, verbose: int = 1):
        self.models = []
        self.scores = []


        testloader = DataLoader(test_dataset, batch_size=128)
        start = time.time()
        for i in range(self.num_models):
            sys.stdout.write(f"\rTraining Model {i + 1}/{self.num_models}")
            print()
            train_sampler = RandomSampler(train_dataset, replacement=True)

            trainloader = DataLoader(dataset=train_dataset, batch_size=128, sampler=train_sampler)
            
            model, accuracy = self.train_model(trainloader, testloader, init_shape, epochs, verbose)
            self.models.append(model)
            self.scores.append(accuracy)

            sys.stdout.flush()
        end = time.time()
        self.train_time = end - start
        





