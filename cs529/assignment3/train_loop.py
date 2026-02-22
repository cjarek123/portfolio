'''
train_loop.py

CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk

USAGE:

call python ./train_loop.py

Type the number of images you wish to train on. This will produce the ./models folder
that can be loaded later with the pickle library.
'''

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn. svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import idx2numpy
import pickle
import os

def train_loop(dataset_name, train_images, train_labels, test_images, test_labels, verbose):
    
    # Reshape input images
    train_images = train_images.reshape(train_images.shape[0], -1)
    test_images = test_images.reshape(test_images.shape[0], -1)

    # Components for PCA
    n_components = [50, 100, 200]
    # Components for LDA

    # Kernel Options
    kernels = ['linear', 'rbf', 'poly']

    # Param grid for GridSearchCV
    c_values = [.001, .01, .1, 1]
    degree = np.arange(1,5)
    gamma = [.0001, .001, .01, .1]
    param_grid_linear = {
        'svc__C': c_values
    }
    param_grid_rbf = {
        'svc__C': c_values,
        'svc__gamma': gamma,
    }
    param_grid_poly = {
        'svc__C': c_values,
        'svc__gamma': gamma,
        'svc__degree': degree,
    }
    results = []
    # for each kernel
    for kernel in kernels:
        # for each component option
        for n in n_components:
            if verbose == 2:
                print(f"Training kernel '{kernel}' for n_components={n} using PCA")
            pipe = Pipeline(
                steps=[('scaler', StandardScaler()), 
                       ('pca', PCA(n_components=n)), 
                       ('svc', SVC(kernel=kernel))])
            
            # Param grid for each kernel
            if kernel == 'linear':
                current_params = param_grid_linear
            elif kernel == 'rbf':
                current_params = param_grid_rbf
            elif kernel == 'poly':
                current_params = param_grid_poly
            else:
                raise Exception("Unkonwn kernel encountered")
            # grid search with appropriate params
            search = GridSearchCV(pipe, current_params, n_jobs=-1, cv=3, verbose=verbose)
            # fit grid search
            search.fit(train_images, train_labels)
            # get best parameters
            best_c = search.best_params_['svc__C']
            best_gamma = None
            if kernel == 'rbf' or kernel == 'poly':
                best_gamma = search.best_params_['svc__gamma']
            best_degree = None if kernel != 'poly' else search.best_params_['svc__degree']
            
            best_pipe = search.best_estimator_

            with open(f"./models/{dataset_name}_{kernel}_n_{n}.pkl", "wb") as f:
                pickle.dump(best_pipe, f)
                f.close()

            # Construct return values
            pred = best_pipe.predict(test_images)
            accuracy = accuracy_score(test_labels, pred)
            results.append({ 'n_components': n, 
                            'kernel': kernel, 
                            'best_c': best_c, 
                            'best_degree': best_degree, 
                            'best_gamma': best_gamma, 
                            'best_score': search.best_score_,
                            'accuracy': accuracy,
                            })
   
    return results

def main(dataset_name, train_images, train_labels, test_images, test_labels, verbose):
    
    # Get results and return as a dataframe
    results = train_loop(dataset_name, train_images, train_labels, test_images, test_labels, verbose)
    results_df = pd.DataFrame(results)
    return results_df 


if __name__ == '__main__':
    samples = None
    # Get desired num samples
    print("Type the number of images to train on:")
    while samples is None:
        try:
            samples = int(input())
        except:
            
            print("Please use integers only")
    # Create model dir to save model files
    try:
        os.mkdir('models')
    except:
        print("Consider deleting an existing models folder before running to avoid overwrites.")
        pass

    print("----------------------------------------")
    print(f"Using {samples} images from each set")
    print("----------------------------------------")

    # Load MNIST
    train_images = idx2numpy.convert_from_file('./mnist/train-images-idx3-ubyte')[0:samples]
    train_labels = idx2numpy.convert_from_file('./mnist/train-labels-idx1-ubyte')[0:samples]
    test_images = idx2numpy.convert_from_file('./mnist/t10k-images-idx3-ubyte')
    test_labels = idx2numpy.convert_from_file('./mnist/t10k-labels-idx1-ubyte')

    # Train MNIST
    print ("Training MNIST")
    df_mnist = main('MNIST', train_images, train_labels, test_images, test_labels, 2)
    df_mnist.to_csv("minst_train_result.csv")

    # Load MNIST Fashion
    train_images = idx2numpy.convert_from_file('./fashion/train-images-idx3-ubyte')[0:samples]
    train_labels = idx2numpy.convert_from_file('./fashion/train-labels-idx1-ubyte')[0:samples]
    test_images = idx2numpy.convert_from_file('./fashion/t10k-images-idx3-ubyte')
    test_labels = idx2numpy.convert_from_file('./fashion/t10k-labels-idx1-ubyte')

    # Train MNIST Fashion
    print("Training Fashion MNIST")

    df_fashion = main('MNIST_FASH',train_images, train_labels, test_images, test_labels, 2)
    df_fashion.to_csv('mnist_fashion_train_result.csv')