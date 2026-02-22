"""
CS 529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import numpy as np
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from regression_tree import RegressionTree

def tune_tree(X, y, random_state = 42):
    max_depth = np.arange(1, 100, 2)
    min_samples_leaf = np.arange(1, 50, 2)

    grid = [[m, l] for m in max_depth for l in min_samples_leaf]

    results = []
    iteration = 0
    total_combinations = len(grid)
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=.2, shuffle=True, random_state=random_state)
    for m, l in grid:
        
        sys.stdout.write(f"\rTesting {iteration + 1}/{total_combinations} combinations")
        reg = RegressionTree(max_depth=m, min_samples_leaf=l)

        reg.fit(X_train, y_train)
        results.append({ 'max_depth': m, 'min_samples_leaf': l, 'MAE': mean_absolute_error(y_test, reg.predict(X_test))})
        iteration += 1
        sys.stdout.flush()
    results_df = pd.DataFrame(results)
    best_max_depth, best_min_samples_leaf, best_mae = results_df[results_df['MAE'] == results_df['MAE'].min()].iloc[0][['max_depth', 'min_samples_leaf', 'MAE']]


    return best_max_depth, best_min_samples_leaf, best_mae