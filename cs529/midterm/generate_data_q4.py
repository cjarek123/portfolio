"""
CS 529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import pandas as pd
import numpy as np

def q4_a(t = 100, x1 = 5, x2 = 5, add_noise = False):
    target_columns = ['delta_x1', 'delta_x2']
    
    data_dict = []
    for _ in range(t):
        x1_next = .9 * x1 - .2 * x2
        x2_next = .2 * x1 + .9 * x2

        data_dict.append({'x1': x1, 'x2': x2, 'x1_next': x1_next, 'x2_next': x2_next})

        x1 = x1_next
        x2 = x2_next


    df = pd.DataFrame(data_dict)
    if add_noise:
        noise = np.random.uniform(.5, 1, size=df[target_columns].shape)
        df[target_columns] = df[target_columns] + noise
    
    return df.dropna()


def q4_b(x):
    z = 0
    result = []
    
    for _ in range(21): # 21 accounts for missing data when shifting later
        if x > 1:
            x = 0
        else:
            x = x + .2
        z = z + x
        result.append({'x': x, 'z': z })
    
    df = pd.DataFrame(result)
    df['x_next'] = df['x'].shift(-1)
    df['z_next'] = df['z'].shift(-1)
    return df.dropna()