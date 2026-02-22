"""
CS 529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import time
from regression_tree import RegressionTree
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import numpy as np
def evaluate_q2(random_state: int = 42):
    # Generate Data
    X = np.random.uniform(-3, 3, 100).reshape(-1, 1)
    y = .8 * np.sin(X - 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=random_state)
    results = []
    # No limitation
    start = time.time()
    reg1 = RegressionTree()
    reg1.fit(X_train, y_train)
    end = time.time()

    preds = reg1.predict(X_test)
    results.append({
        'Model': 'No Limit Regression',
        'Time': end - start,
        'MAE': mean_absolute_error(y_test, preds),
        'Height': reg1.get_height(reg1.root)
    })
    # 1/2 of the obtained height
    half_height = np.round(reg1.get_height(reg1.root) / 2)
    three_quarter = np.round(reg1.get_height(reg1.root) * (3/4))

    start = time.time()
    reg2 = RegressionTree(max_depth=half_height)
    reg2.fit(X_train, y_train)
    end = time.time()

    preds = reg2.predict(X_test)
    results.append({
        'Model': '1/2 Of Obtained Height',
        'Time': end - start,
        'MAE': mean_absolute_error(y_test, preds),
        'Height': reg2.get_height(reg2.root)
    })
    # 3/4 of the obtained height
    start = time.time()
    reg3 = RegressionTree(max_depth=three_quarter)
    reg3.fit(X_train, y_train)
    end = time.time()

    preds = reg3.predict(X_test)
    results.append({
        'Model': '3/4 Of Obtained Height',
        'Time': end - start,
        'MAE': mean_absolute_error(y_test, preds),
        'Height': reg3.get_height(reg3.root)
    })
    leaf_sizes = [2, 4, 8]
    for min_samples_leaf in leaf_sizes:
        start = time.time()
        reg = RegressionTree(min_samples_leaf=min_samples_leaf)
        reg.fit(X_train, y_train)
        end = time.time()

        preds = reg.predict(X_test)

        results.append({
        'Model': f'{min_samples_leaf} Samples Per Leaf',
            'Time': end - start,
            'MAE': mean_absolute_error(y_test, preds),
            'Height': reg.get_height(reg.root) 
        })
    

    return results