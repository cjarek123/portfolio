"""
CS529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
from nltk.stem.porter import PorterStemmer
from review_dataset import ReviewDataset
import torch
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import re
from torch.utils.data import DataLoader
from typing import TypedDict
from nltk.corpus import stopwords
stop = stopwords.words('english')




porter = PorterStemmer()
def tokenize_porter(text):
    return [porter.stem(word) for word in text.split()]

def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\\)|\\(|D|P)', text)
    text = (re.sub('[\\W]+', ' ', text.lower()) + ''.join(emoticons).replace('-', ''))
    return text

RANDOM_SEED = 100



class ReviewData(TypedDict):

    test_data: DataLoader
    train_data: DataLoader
    test_dataset: ReviewDataset
    train_dataset: ReviewDataset
    X_test: torch.Tensor
    y_test: torch.Tensor
    init_shape: int
def load_review_data(subset: int = 0, batch_size: int = 128) -> ReviewData:
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    df = pd.read_csv('movie_data.csv', encoding='utf-8')
    if subset > 0 and subset <= 50000:
        df = df.iloc[0:subset]
    df['review'] = df['review'].apply(preprocessor)
    
    X_train, X_test, y_train, y_test = train_test_split(df['review'].values, df['sentiment'].values, test_size=.3, random_state=RANDOM_SEED, stratify=df['sentiment'].values)

    tfidf = TfidfVectorizer(max_features=2500, strip_accents=None, lowercase=False, preprocessor=None, stop_words=stop)

    X_train = tfidf.fit_transform(X_train)
    X_test = tfidf.transform(X_test)

    X_train = torch.tensor(X_train.toarray(), dtype=torch.float32)
    y_train = torch.from_numpy(y_train)

    print("Class Distribution:", torch.bincount(y_train))

    X_test = torch.tensor(X_test.toarray(), dtype=torch.float32)
    y_test = torch.from_numpy(y_test)

    train_dataset = ReviewDataset(X_train, y_train)
    train_data = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    test_dataset = ReviewDataset(X_test, y_test)
    test_data = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    init_shape = X_train.shape[1]

    return { 'X_test': X_test, 'y_test': y_test, 'train_data': train_data, 'train_dataset': train_dataset, 'test_dataset': test_dataset, 'test_data': test_data, 'init_shape': init_shape, }

