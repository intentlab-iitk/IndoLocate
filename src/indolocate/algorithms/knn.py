import logging
import numpy as np
import tensorflow as tf
from .base import Algorithm

# Algorithms
class kNN(Algorithm):
    def __init__(self):
        super().__init__(algorithm="kNN")
        self._configure("knn.yaml")

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        self.model = {
            "k": self.config["k"],
            "order": self.config["order"],
            "X_train": None,
            "Y_train": None,
        }
        num_samples = X_train.shape[0]
        self.model["X_train"] = tf.constant(X_train.reshape(num_samples, -1), dtype=tf.float32)
        self.model["Y_train"] = tf.constant(Y_train, dtype=tf.float32)
        logging.info(f"Model trained with {X_train.shape[0]} samples.")

    def predict(self, X_sample: np.ndarray) -> np.ndarray:
        if self.model["X_train"] is None or self.model["Y_train"] is None:
            logging.error("Model is not trained. Call fit() before predict().")
            raise ValueError("Model is not trained. Call fit() before predict().")
        X_sample = tf.convert_to_tensor(X_sample, dtype=tf.float32)
        X_sample_flat = tf.reshape(X_sample, (1, -1))
        distances = tf.norm(self.model["X_train"] - X_sample_flat, ord=self.model["order"], axis=1)
        knn_indices = tf.argsort(distances)[:self.model["k"]]
        knn_labels = tf.gather(self.model["Y_train"], knn_indices)
        prediction = np.array(tf.reduce_mean(knn_labels, axis=0))

        return prediction
