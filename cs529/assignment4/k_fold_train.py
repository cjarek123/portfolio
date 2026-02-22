"""
CS529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import torch
from FNN import FNN
from load_review_data import load_review_data
from sklearn.model_selection import KFold
from torch.utils.data import ConcatDataset, DataLoader
import torch.nn as nn
import os
from review_dataset import ReviewDataset
import time


def run_kfold(train_dataset: ReviewDataset, test_dataset: ReviewDataset, init_shape: int, k: int = 5, epochs: int = 50, verbose: int = 0):
    try:
        os.mkdir("k_fold_models")
    except:
        pass
    k_folds = k


    dataset = ConcatDataset([train_dataset, test_dataset])

    results = {}
    time_costs = []


    kfold = KFold(n_splits=k_folds, shuffle=True)
    print("-"*30)

    for fold, (train_ids, test_ids) in enumerate(kfold.split(dataset)):

        print(f"FOLD {fold}")
        print("-"*30)

        train_subsampler = torch.utils.data.SubsetRandomSampler(train_ids)
        test_subsampler = torch.utils.data.SubsetRandomSampler(test_ids)

        trainloader = DataLoader(dataset, batch_size=128, sampler=train_subsampler)
        testloader = DataLoader(dataset, batch_size=128, sampler=test_subsampler)


        model = FNN(init_shape, learning_rate=.0001)

        


        model.reset_weights()


        model.fit(trainloader, epochs=epochs, verbose=verbose)
        time_costs.append(model.train_time)
               
        print("Training process has finished. Saving trained model.")
        print("Starting Testing")


        save_path = f'./k_fold_models/model-fold-{fold}.pth'
        model.save_model(save_path)


        accuracy = model.evaluate(testloader)


        print("Accuracy for fold %d: %d %%" % (fold, accuracy))
        print("-"*30)
        results[fold] = accuracy

    print(f'K-FOLD CROSS VALIDATION RESULTS FOR {k_folds} FOLDS')
    print('-'*10)

    sum = 0.0

    for key, value in results.items():
        print(f'Fold {key}: {value} %')
        sum += value
    
    print(f'Average: {sum/len(results.items())} %')

    return results, time_costs