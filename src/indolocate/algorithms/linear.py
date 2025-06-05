import logging
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from .base import Algorithm

class LinearRegressor(Algorithm):
    def __init__(self):
        super().__init__()
        self._configure("linear_reg.yaml")

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        try:
            X_train = np.nan_to_num(X_train, nan=-120, posinf=-120, neginf=-120)
            X_train = np.clip(X_train, -120, 0)

            self._scaler = StandardScaler()
            X_train = self._scaler.fit_transform(X_train)

            self.model = LinearRegression(fit_intercept=self.config.get("fit_intercept", True))
            self.model.fit(X_train, Y_train)

        except Exception as e:
            logging.error(f"Fit failed: {e}")
            raise

    def predict(self, X_sample: np.ndarray) -> np.ndarray:
        try:
            X_sample = np.nan_to_num(X_sample, nan=-120, posinf=-120, neginf=-120)
            X_sample = np.clip(X_sample, -120, 0)
            X_sample = np.atleast_2d(X_sample)

            X_sample = self._scaler.transform(X_sample)

            prediction = self.model.predict(X_sample)
            return prediction[0] if X_sample.shape[0] == 1 else prediction

        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise

class RidgeRegressor(Algorithm):
    def __init__(self):
        super().__init__()
        self._configure("ridge_reg.yaml")

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        try:
            X_train = np.nan_to_num(X_train, nan=-120, posinf=-120, neginf=-120)
            X_train = np.clip(X_train, -120, 0)

            self._scaler = StandardScaler()
            X_train = self._scaler.fit_transform(X_train)

            self.model = Ridge(
                alpha=self.config.get("alpha", 1.0),
                fit_intercept=self.config.get("fit_intercept", True)
            )
            self.model.fit(X_train, Y_train)

        except Exception as e:
            logging.error(f"Fit failed: {e}")
            raise

    def predict(self, X_sample: np.ndarray) -> np.ndarray:
        try:
            X_sample = np.nan_to_num(X_sample, nan=-120, posinf=-120, neginf=-120)
            X_sample = np.clip(X_sample, -120, 0)
            X_sample = np.atleast_2d(X_sample)

            X_sample = self._scaler.transform(X_sample)

            prediction = self.model.predict(X_sample)
            return prediction[0] if X_sample.shape[0] == 1 else prediction

        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise

class LassoRegressor(Algorithm):
    def __init__(self):
        super().__init__()
        self._configure("lasso_reg.yaml")

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        try:
            X_train = np.nan_to_num(X_train, nan=-120, posinf=-120, neginf=-120)
            X_train = np.clip(X_train, -120, 0)

            self._scaler = StandardScaler()
            X_train = self._scaler.fit_transform(X_train)

            self.model = Lasso(
                alpha=self.config.get("alpha", 1.0),
                fit_intercept=self.config.get("fit_intercept", True)
            )
            self.model.fit(X_train, Y_train)

        except Exception as e:
            logging.error(f"Fit failed: {e}")
            raise

    def predict(self, X_sample: np.ndarray) -> np.ndarray:
        try:
            X_sample = np.nan_to_num(X_sample, nan=-120, posinf=-120, neginf=-120)
            X_sample = np.clip(X_sample, -120, 0)
            X_sample = np.atleast_2d(X_sample)

            X_sample = self._scaler.transform(X_sample)

            prediction = self.model.predict(X_sample)
            return prediction[0] if X_sample.shape[0] == 1 else prediction

        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise
