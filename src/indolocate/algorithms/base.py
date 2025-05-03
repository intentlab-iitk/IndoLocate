# Import packages
import os
import yaml
import pickle
import logging
import numpy as np
from typing import Any
import importlib.resources as pkg_resources

class Algorithm:
    def __init__(self, algorithm: str):
        self.name: str = algorithm
        self.config: dict | None = None
        self.model: Any = None
        logging.info(f"Initializing {self.name} model")

    def _configure(self, config_file: str):
        try:
            with pkg_resources.files("indolocate.algorithms.configs").joinpath(config_file).open('r') as file:
                self.config = yaml.safe_load(file) or {}
            logging.info(f"Loaded configuration for {self.name} from package")
        except FileNotFoundError:
            logging.error(f"Configuration file '{config_file}' not found in package.")
            exit
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file '{config_file}' from package: {e}")
            exit

    def configure(self, config_file: str) -> None:
        """
        Load and set configuration from a YAML file.
        """
        try:
            with open(config_file, 'r') as file:
                self.config = yaml.safe_load(file) or {}
            logging.info(f"Loaded configuration from {config_file}")
        except FileNotFoundError:
            logging.error(f"Error find the file {config_file}")
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file '{config_file}': {e}")

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)

        logging.info(f"{self.name} model saved to {path}")

    def load(self, path: str):
        """
        Load the model from specified pickel file.
        """
        with open(path, "rb") as f:
            model_data = pickle.load(f)

        self.model = model_data.model
        self.config = model_data.config
        self.name = model_data.name

        logging.info(f"{self.name} model loaded from {path}")

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        """
        Fit the model with given data.
        """
        self.model(X_train, Y_train)

    def predict(self, X_sample: np.ndarray) -> np.ndarray:
        """
        Predicts the location for the given sample using the model.
        """
        self.model.predit(X_sample)
