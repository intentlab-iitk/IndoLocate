import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from indolocate.utils import load_config 

class RFRegression:
    def __init__(self, file_config=None):
        """
        Initialize the Random Forest Regression model.

        Parameters:
        file_config (str, optional): Path to the YAML configuration file. If None, default settings are used.
        """
        self.name = "RF"

        print(f"[*] Intializing {self.name} model")

        self.config = load_config("indolocate/configs/rf.yaml", file_config)
        self.model = RandomForestRegressor(
            n_estimators=self.config["parameters"]["n_estimators"],
            criterion=self.config["parameters"]["criterion"],
            random_state=42
        )
        
    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        """
        Fit the Random Forest model with training data.

        Parameters:
        X_train (numpy.ndarray): Training data features.
        Y_train (numpy.ndarray): Training data labels.
        """
        self.model.fit(X_train, Y_train)
        print(f"[*] Model trained with {X_train.shape[0]} samples.")

    def predict(self, X_test: np.ndarray):
        """
        Predict the Longitude and Latitude for test data.

        Parameters:
        X_test (numpy.ndarray): Test data features.

        Returns:
        numpy.ndarray: Predicted Longitude and Latitude for test data (shape: [n_samples, 2]).
        """
        # Predict using the trained Random Forest model.
        predictions = self.model.predict(X_test)
        return predictions

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
