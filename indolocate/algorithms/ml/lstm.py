import pickle
import numpy as np
import tensorflow as tf
from keras.api.models import Sequential
from keras.api.layers import LSTM, Dense
from indolocate.utils import load_config

class LSTMRegression:
    def __init__(self, file_config=None):
        """
        Initialize the LSTM Regression model.

        Parameters:
        file_config (str, optional): Path to the YAML configuration file. If None, default settings are used.
        """
        self.name = "LSTM"

        print(f"[*] Intializing {self.name} model")
        self.config = load_config("indolocate/configs/lstm.yaml", file_config)
        
        # The configuration file should specify these parameters, otherwise defaults are used.
        self.n_units = self.config["parameters"]["n_units"]  # Number of LSTM units
        self.activation = self.config["parameters"]["activation"]  # Activation function
        self.optimizer = self.config["parameters"]["optimizer"]  # Optimizer
        self.loss = self.config["parameters"]["loss"]  # Loss function
        self.epochs = self.config["parameters"]["epochs"]  # Number of epochs
        self.batch_size = self.config["parameters"]["batch_size"]  # Batch size
        
        # Initialize the LSTM model
        self.model = self._build_model()

    def _build_model(self):
        """
        Build the LSTM model architecture.

        Returns:
        tf.keras.Model: Compiled LSTM model.
        """
        model = Sequential()
        model.add(LSTM(self.n_units, activation=self.activation, input_shape=(None, 1)))  # Input shape: (timesteps, features)
        model.add(Dense(3))  # Output layer with 3 units (X, Y, Z)
        model.compile(optimizer=self.optimizer, loss=self.loss)
        return model

    def reshape_data(X_train: np.ndarray, Y_train: np.ndarray, time_steps: int):
        """
        Reshape X_train and Y_train for LSTM.

        Parameters:
        - X_train (np.ndarray): Feature matrix of shape (num_samples, num_features).
        - Y_train (np.ndarray): Label matrix of shape (num_samples, output_dim).
        - time_steps (int): Number of time steps for LSTM.

        Returns:
        - X_lstm (np.ndarray): Reshaped features of shape (num_samples - time_steps + 1, time_steps, num_features).
        - Y_lstm (np.ndarray): Reshaped labels of shape (num_samples - time_steps + 1, output_dim).
        """
        num_samples, num_features = X_train.shape
        if len(Y_train.shape) == 1:
            Y_train = Y_train.reshape(-1, 1)  # Ensure Y_train is 2D

        output_dim = Y_train.shape[1]

        if num_samples < time_steps:
            raise ValueError("Number of samples must be greater than or equal to time_steps.")

        X_lstm = np.array([X_train[i:i + time_steps] for i in range(num_samples - time_steps + 1)])
        Y_lstm = np.array([Y_train[i + time_steps - 1] for i in range(num_samples - time_steps + 1)])  # Taking the last value of each sequence

        return X_lstm, Y_lstm

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        """
        Fit the LSTM model with training data.

        Parameters:
        X_train (numpy.ndarray): Training data features of shape (n_samples, features).
        Y_train (numpy.ndarray): Training data labels of shape (n_samples, labels).
        """
        # Reshape X_train to (n_samples, timesteps, features)
        if len(X_train.shape) == 2:
            X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])  # (697, 1, 992)

        # Fit the model using the provided training data
        self.model.fit(X_train, Y_train, epochs=self.epochs, batch_size=self.batch_size, verbose=1)
        print("[#] Model Trained")

    def predict(self, X_test: np.ndarray):
        """
        Predict the outputs (X, Y, Z) for test data.

        Parameters:
        X_test (numpy.ndarray): Test data features of shape (n_samples, features).

        Returns:
        numpy.ndarray: Predicted outputs for test data (shape: [n_samples, 3]).
        """
        # Reshape X_test to (n_samples, timesteps, features)
        if len(X_test.shape) == 2:
            X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])  # (n_samples, 1, 992)

        # Predict using the trained LSTM model
        predictions = self.model.predict(X_test)
        return predictions

    def save(self, file_path: str):
        """
        Save the LSTM model to a file.

        Parameters:
        file_path (str): Path to save the model.
        """
        # Save the model and configuration using pickle
        model_data = {
            "model": self.model,
            "config": self.config,
        }
        with open(file_path, "wb") as f:
            pickle.dump(model_data, f)
        print(f"[#] LSTM model saved to {file_path}")

    def load(self, file_path: str):
        """
        Load the LSTM model from a file.

        Parameters:
        file_path (str): Path to load the model from.
        """
        with open(file_path, "rb") as f:
            model_data = pickle.load(f)
        self.model = model_data["model"]
        self.config = model_data["config"]
        print(f"[#] LSTM model loaded from {file_path}")



