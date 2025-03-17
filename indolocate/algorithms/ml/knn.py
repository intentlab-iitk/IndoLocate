import pickle
import tensorflow as tf
import numpy as np
from indolocate.utils import load_config
from indolocate.utils import preprocess_rssi

class kNNRegression:
    def __init__(self, file_config=None):
        """
        Initialize the kNN Regression model.

        Parameters:
        file_config (str, optional): Path to the YAML configuration file. If None, default settings are used.
        """
        self.name = "kNN"

        print(f"[*] Intializing {self.name} model")

        self.config = load_config("indolocate/configs/knn.yaml", file_config)
        self.model = {
            "k": self.config["parameters"]["k"],
            "order": self.config["parameters"]["order"],
            "X_train": None,
            "Y_train": None,
        }

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        """
        Fit the model with training data.

        Parameters:
        X_train (numpy.ndarray): Training data features.
        Y_train (numpy.ndarray): Training data labels.
        """
        self.model["X_train"] = tf.constant(X_train, dtype=tf.float32)
        self.model["Y_train"] = tf.constant(Y_train, dtype=tf.float32)

        print(f"[*] Model trained with {X_train.shape[0]} samples.")

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the Location for test data.

        Parameters:
        X_test (numpy.ndarray): Test data features.

        Returns:
        numpy.ndarray: Predicted Location for test data.
        """
        if self.model["X_train"] is None or self.model["Y_train"] is None:
            raise ValueError("[!] Model is not trained. Call fit() before predict().")

        X_test = tf.constant(X_test, dtype=tf.float32)
        predictions = []

        for test_sample in X_test:
            # Compute distances between the test sample and all training samples
            distances = tf.norm(self.model["X_train"] - test_sample, ord=self.model["order"], axis=1)

            # Find the indices of the K nearest neighbors
            knn_indices = tf.argsort(distances)[: self.model["k"]]

            # Retrieve the labels of the K nearest neighbors
            knn_labels = tf.gather(self.model["Y_train"], knn_indices)

            # Compute the mean of the K nearest neighbors' labels as the prediction
            prediction = tf.reduce_mean(knn_labels, axis=0) 
            predictions.append(prediction)

        return tf.stack(predictions).numpy()

    def save(self, file_path: str):
        """
        Save the entire model to a file.

        Parameters:
        file_path (str): Path to save the model.
        """
        with open(file_path, "wb") as f:
            pickle.dump(self, f)

        print(f"[*] {self.name} model saved to {file_path}")

    def load(self, file_path: str):
        """
        Load the model from a file.

        Parameters:
        file_path (str): Path to load the model from.
        """
        with open(file_path, "rb") as f:
            model_data = pickle.load(f)

        self.model = model_data.model
        self.config = model_data.config
        self.name = model_data.name

        print(f"[*] {self.name} model loaded with {file_path}")
