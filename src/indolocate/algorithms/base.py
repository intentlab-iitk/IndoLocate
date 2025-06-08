"""
File            : indolocate/algorithms/base.py   
Description     : Contains common funcs and class for algorithm module.  
"""

# Import packages
import os
import yaml
import pickle
import logging
import numpy as np
from typing import Any
import importlib.resources as pkg_resources

class Algorithm:
    def __init__(self):
        self.name: str = self.__class__.__name__
        self.config: dict | None = None
        self.model = None
        logging.info(f"Initializing {self.name} model")

    def _configure(self, config_file: str):
        """
        Internal package configuration for models.
        """
        try:
            with pkg_resources.files("indolocate.algorithms.configs").joinpath(config_file).open('r') as file:
                self.config = yaml.safe_load(file) or {}
            logging.info(f"Loaded configuration for {self.name} from package")
        except FileNotFoundError:
            logging.error(f"Configuration file '{config_file}' not found in package.")
            return
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file '{config_file}' from package: {e}")
            return

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
        Load attributes from the specified pickle file into this instance.
        """
        with open(path, "rb") as f:
            loaded = pickle.load(f)

        self.__dict__.update(loaded.__dict__)
        logging.info(f"{self.name} model loaded from {path}")

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        """
        Fit the model with given data.
        """
        X_train = np.array(X_train)
        Y_train = np.array(Y_train)
        class RandomModel:
            def predict(self, X_sample):
                x = np.random.uniform(-7, 20)
                y = np.random.uniform(-18, 5)
                return np.array([x, y])

        self.model = RandomModel()
        logging.info(f"{self.name} model fitted with {X_train.shape[0]} samples")

    def predict(self, X_sample: np.ndarray) -> np.ndarray:
        """
        Predicts the location for the given sample using the model.
        """
        return self.model.predict(X_sample)
