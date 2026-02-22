"""
CS529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import pyprind
import pandas as pd
import os
import sys
import numpy as np

basepath = 'aclImdb'

labels = { 'pos': 1, 'neg': 0 }
columns = ['review', 'sentiment']

pbar = pyprind.ProgBar(50000, stream=sys.stdout)


df = pd.DataFrame(columns=columns)

for s in ('test', 'train'):
    for l in ('pos', 'neg'):
        path = os.path.join(basepath, s, l)
        for file in sorted(os.listdir(path)):
            with open(os.path.join(path, file), 'r', encoding='utf-8') as infile:
                txt = infile.read()
                temp = pd.DataFrame([[txt, labels[l]]], columns=columns)
                df = pd.concat([df, temp])
                pbar.update()
                infile.close()
np.random.seed(0)
df = df.reindex(np.random.permutation(df.index))
df.to_csv('movie_data.csv', index=False, encoding='utf-8')