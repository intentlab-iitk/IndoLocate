import pickle
import numpy as np
from keras.api import Sequential
from keras.api.layers import Input, Dense
from keras.api.optimizers import Adam
from indolocate.utils import load_config

class DNNRegression:
    def __init__(self, file_config=None):
        """
        Initialize the DNN Regression model.

        Parameters:
        file_config (str): Path to the YAML configuration file. If None, default settings are used.
        """
        self.name = "DNN"

        print(f"[*] Intializing {self.name} model")

        self.config = load_config("indolocate/configs/dnn.yaml", file_config)
        self.model = self._build_model()

    def _build_model(self):
        """
        Build the Sequential DNN model based on the configuration.
        """
        model = Sequential()

        # Define Input Layer 
        model.add(Input(shape=(self.config["parameters"]["input_dim"],)))

        # Hidden Layers
        if self.config["parameters"]["hidden_layers"]:
            for units in self.config["parameters"]["hidden_layers"]:
                model.add(Dense(units, activation=self.config["parameters"]["activation"]))

        # Add Output Layer
        model.add(Dense(self.config["parameters"]["output_dim"], activation='linear'))

        # Compile Model
        model.compile(
            optimizer=Adam(learning_rate=self.config["parameters"]["learning_rate"]), 
            loss=self.config["parameters"]["loss"]
        )

        return model


    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        """
        Fit the model with training data.

        Parameters:
        X_train (numpy.ndarray): Training data features.
        Y_train (numpy.ndarray): Training data labels.
        """
        self.model.fit(
            X_train, Y_train, 
            epochs=self.config["parameters"]["epochs"], 
            batch_size=self.config["parameters"]["batch_size"],
        )
        print(f"[*] Model trained with {X_train.shape[0]} samples.")

    def predict(self, X_test: np.ndarray):
        """
        Predict using the trained DNN model.

        Parameters:
        X_test (numpy.ndarray): Test data features.

        Returns:
        numpy.ndarray: Predictions from the model.
        """
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