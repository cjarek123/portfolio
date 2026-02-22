"""
CS 529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""

import time
import numpy as np
import pandas as pd
from sklearn.svm import LinearSVC
from make_classification import make_classification
import matplotlib.pyplot as plt

def eval(X_train, X_test, y_train, y_test, dual):
    model = LinearSVC(dual=dual, loss='squared_hinge' if not dual else 'hinge', random_state=42)
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    y_pred = model.predict(X_test)
    accuracy = np.sum(y_pred == y_test) / len(y_test)
    return train_time, accuracy

def main():
    d_values = [10, 50, 100, 500, 1000]
    n_values = [500, 1000, 5000, 10000, 100000]
    results = []

    for d in d_values:
        for n in n_values:
            X_train, X_test, y_train, y_test, _, _ = make_classification(d=d, n=n, u=100, random_state=42)

            time_primal, accuracy_primal = eval(X_train, X_test, y_train, y_test, dual=False)
            time_dual, accuracy_dual = eval(X_train, X_test, y_train, y_test, dual=True)

            results.append([d, n, time_primal, accuracy_primal, time_dual, accuracy_dual])

    out = pd.DataFrame(results, columns=["D", "N", "Time Primal", "Accuracy Primal", "Time Dual", "Accuracy Dual"])
    out.to_csv("svm_comparison_results.csv", index=False)
    print(out)

    # Times
    plt.figure(figsize=(10, 5))
    plt.bar(out.index - 0.2, out["Time Primal"], width=0.4, label="Time Primal", color='blue')
    plt.bar(out.index + 0.2, out["Time Dual"], width=0.4, label="Time Dual", color='red')
    plt.xlabel("Dataset")
    plt.ylabel("Training Time (seconds)")
    plt.title("Time")
    plt.legend()
    plt.xticks(out.index, [f"d={d}, n={n}" for d, n in zip(out["D"], out["N"])], rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("time_plot.png")
    plt.show()

    # Accuracy
    plt.figure(figsize=(10, 5))
    plt.bar(out.index-0.2, out["Accuracy Primal"], width=0.4, label="Time Primal", color='blue')
    plt.bar(out.index+0.2, out["Accuracy Dual"], width=0.4, label="Time Dual", color='red')
    plt.xlabel("Dataset")
    plt.ylabel("Accuracy")
    plt.title("Accuracy")
    plt.legend()
    plt.xticks(out.index, [f"d={d}, n={n}" for d, n in zip(out["D"], out["N"])], rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("accuracy_plot.png")
    plt.show()

if __name__ == "__main__":
    main()
