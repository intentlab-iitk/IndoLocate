"""
File            : indolocate/algorithms/knn.py  
Description     : Implementation of kNN algorithm.  
"""

# Imports
import logging
import numpy as np
import tensorflow as tf
from .base import Algorithm

class kNNRegressor(Algorithm):
    def __init__(self):
        super().__init__()
        self._configure("knn.yaml")

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        try:
            self.model = {
                "k": self.config.get("k", 3),
                "order": self.config.get("order", 2),
                "X_train": tf.constant(X_train, dtype=tf.float32),
                "Y_train": tf.constant(Y_train, dtype=tf.float32),
            }

            logging.info(f"{self.name} model trained with {X_train.shape[0]} samples.")
        except Exception as e:
            logging.error(f"Fit failed: {e}")
            raise

    def predict(self, X_sample: np.ndarray) -> np.ndarray:
        try:
            if self.model["X_train"] is None or self.model["Y_train"] is None:
                raise ValueError("Model is not trained. Call fit() before predict().")

            X_sample_tensor = tf.convert_to_tensor(np.atleast_2d(X_sample), dtype=tf.float32)
            distances = tf.norm(self.model["X_train"] - X_sample_tensor, ord=self.model["order"], axis=1)
            knn_indices = tf.argsort(distances)[:self.model["k"]]
            knn_labels = tf.gather(self.model["Y_train"], knn_indices)
            prediction = tf.reduce_mean(knn_labels, axis=0)

            return prediction.numpy()
        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise
