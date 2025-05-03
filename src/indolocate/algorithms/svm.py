import sklearn.svm
import numpy as np
from .base import Algorithm

class SVM(Algorithm):
    def __init__(self):
        super().__init__(algorithm="SVM")

        params = self.config.get("parameters", {})
        self.model = sklearn.svm(
            kernel=params.get("kernel", "rbf"),
            C=params.get("C", 1.0),
            epsilon=params.get("epsilon", 0.1)
        )

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        X_flat = X_train.reshape(X_train.shape[0], -1)
        self.model.fit(X_flat, Y_train)

    def predict(self, X_sample: np.ndarray):
        X_flat = X_sample.reshape(1, -1)
        return self.model.predict(X_flat)
    