import pickle
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from indolocate.utils import load_config 

class GBDTRegression:
    def __init__(self, file_config=None):
        """
        Initialize the Gradient Boosted Decision Trees (GBDT) multi-output regression model.

        Parameters:
        file_config (str): Path to the YAML configuration file. If None, default settings are used.
        """
        print("[#] Gradient Boosted Decision Trees model initialized")
        self.title = "Gradient Boosted Decision Trees"
        
        # Load configuration; default configuration file is assumed to be at this path.
        self.config = load_config("indolocate/configs/gbdt.yaml", file_config)
        
        # Load parameters from the config file, using defaults if not specified.
        self.n_estimators = self.config["parameters"]["n_estimators"]
        self.loss = self.config["parameters"]["loss"]
        
        # Initialize the GBDT model with MultiOutputRegressor
        base_model = GradientBoostingRegressor(
            n_estimators=self.n_estimators,
            loss=self.loss,
            random_state=42
        )
        self.model = MultiOutputRegressor(base_model)
        
    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        """
        Train the GBDT model with training data.

        Parameters:
        X_train (numpy.ndarray): Training data features.
        Y_train (numpy.ndarray): Training data labels (multi-output support).
        """
        self.model.fit(X_train, Y_train)
        print("[#] GBDT model trained")

    def predict(self, X_test: np.ndarray):
        """
        Predict multiple outputs for test data.

        Parameters:
        X_test (numpy.ndarray): Test data features.

        Returns:
        numpy.ndarray: Predicted values for multiple outputs.
        """
        predictions = self.model.predict(X_test)
        return predictions

    def save(self, file_path: str):
        """
        Save the trained multi-output GBDT model to a file.

        Parameters:
        file_path (str): Path to save the model.
        """
        model_data = {
            "model": self.model,
            "config": self.config,
        }
        with open(file_path, "wb") as f:
            pickle.dump(model_data, f)
        print(f"[#] GBDT model saved to {file_path}")

    def load(self, file_path: str):
        """
        Load a trained multi-output GBDT model from a file.

        Parameters:
        file_path (str): Path to load the model from.
        """
        with open(file_path, "rb") as f:
            model_data = pickle.load(f)
        self.model = model_data["model"]
        self.config = model_data["config"]
        print(f"[#] GBDT model loaded from {file_path}")
