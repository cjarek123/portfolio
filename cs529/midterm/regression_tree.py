"""
CS 529
Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import numpy as np
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # This can now be a vector (multi-output)

class RegressionTree:
    def __init__(self, max_depth=None, min_samples_leaf=1):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.root = None

    def fit(self, X, y):
        self.root = self._build_tree(X, y, depth=0)

    def _build_tree(self, X, y, depth):
        num_samples, num_features = X.shape

        # Stopping conditions
        if num_samples <= self.min_samples_leaf or (self.max_depth is not None and depth >= self.max_depth):
            return Node(value=np.mean(y, axis=0))

        best_feature, best_threshold = self._find_best_split(X, y)
        if best_feature is None:
            return Node(value=np.mean(y, axis=0))

        left_indices = X[:, best_feature] <= best_threshold
        right_indices = ~left_indices

        left_subtree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_subtree = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return Node(feature=best_feature, threshold=best_threshold, left=left_subtree, right=right_subtree)

    def get_height(self, next: Node = None):
        if next is None:
            return 0
        
        left_height = self.get_height(next.left)
        right_height = self.get_height(next.right)

        return 1 + np.max([left_height, right_height])

    def _find_best_split(self, X, y):
        num_samples, num_features = X.shape
        best_feature, best_threshold, best_sse = None, None, float('inf')

        for feature in range(num_features):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask

                if sum(left_mask) < self.min_samples_leaf or sum(right_mask) < self.min_samples_leaf:
                    continue

                sse = self._compute_sse(y[left_mask], y[right_mask])
                if sse < best_sse:
                    best_feature, best_threshold, best_sse = feature, threshold, sse

        return best_feature, best_threshold

    def _compute_sse(self, y_left, y_right):
        def sse(y):
            return np.sum((y - np.mean(y, axis=0)) ** 2)

        return sse(y_left) + sse(y_right)

    def predict(self, X):
        return np.array([self._predict_sample(x, self.root) for x in X])

    def _predict_sample(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)