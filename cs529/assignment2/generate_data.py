"""
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
run as python generate_data.py

will generate 25 files in a ./data dir
this is added to the gitignore so it won't be pushed to the repo

Don't try to push the output files to the repo, it's kind of massive for CSV's.
"""
from make_classification import make_classification
import pandas as pd
import os
import shutil
d_range = [10, 50, 100, 500, 1000]
n_range = [500, 1000, 5000, 10000, 100000]




combinations = [[d, n] for d in d_range for n in n_range]

print(f"Writing data for {len(combinations)} combinations")


if os.path.exists("data/"):
    shutil.rmtree("data/")
    os.mkdir("data/")
else:
    os.mkdir("data/")

for c in combinations:
    d = c[0]
    n = c[1]

    X_train, X_test, y_train, y_test, data, labels = make_classification(d=d, n=n, u=100, random_state=42)

    df = pd.DataFrame(data=data, columns=[f"X_{i+1}" for i in range(d)])
    df['target'] = labels
    
    print(f"Writing d = {d}, n = {n} to CSV")
    df.to_csv(f'./data/d-{d}-n-{n}.csv')