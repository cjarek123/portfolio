"""
CS529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import torch
from torch.utils.data import DataLoader
from torch import Tensor
import sys
import time

class FNN:


    def __init__(self, init_shape: int, learning_rate: float = .0001, weight_decay: float = 0):
        self.learning_rate = learning_rate;
        self.weight_decay = weight_decay
        self.init_shape = init_shape
        self.model = self.init_model_()
        self.loss_function = torch.nn.CrossEntropyLoss()
        self.train_loss = []
        self.train_accuracy = []
        self.train_time = 0







    def fit(self, train_data: DataLoader, epochs = 50, verbose = 0):
        
        size = len(train_data.dataset)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate, weight_decay=self.weight_decay)
        start = time.time()
        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            if verbose == 0:
                sys.stdout.write(f"\rEpoch {epoch + 1}/{epochs}")
            self.model.train()
            for (x, y) in train_data:
                output = self.model(x)

                pred = torch.argmax(output, dim=1)
                correct += (pred == y).sum()

                loss = self.loss_function(output, y)
                loss.backward()
                total_loss += loss.item()
                optimizer.step()
                self.model.zero_grad()
            accuracy = 100. * correct / size
            self.train_accuracy.append(accuracy)
            if verbose == 1:
                print(f"Epoch {epoch + 1}/{epochs}: Training Loss = {total_loss} | Accuracy: {accuracy}")
                self.train_loss.append(total_loss)
            else:
                sys.stdout.flush()
        end = time.time()
        self.train_time = end - start
        if verbose == 0 or verbose == 1:
            print()

    def predict(self, input: Tensor):
        output = self.model(input)
        preds = torch.argmax(output, dim=1)
        return preds
    
    def evaluate(self, test_data: DataLoader):

        self.model.eval()
        test_loss = 0
        correct = 0
        total_samples = 0
        with torch.no_grad():
            for (x, y) in test_data:
                output = self.model(x)

                test_loss += self.loss_function(output, y)
                pred = torch.argmax(output, dim=1)
                correct += (pred == y).sum().item()
                total_samples += x.size(0)
        accuracy = float(100. * correct / total_samples)
        return accuracy

    def reset_weights(self):

        for layer in self.model.children():
            if hasattr(layer, 'reset_parameters'):
                print(f'Reset trainable parameters of layer = {layer}')
                layer.reset_parameters()

    def save_model(self, path: str):
        torch.save(self.model.state_dict(), path)
    def init_model_(self): 
        model = torch.nn.Sequential(
        torch.nn.Linear(self.init_shape, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 2),
        )
        return model
    

