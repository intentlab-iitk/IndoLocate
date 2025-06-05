import logging
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from .base import Algorithm

class PolynomialRegressor(Algorithm):
    def __init__(self):
        super().__init__()
        self._configure("polynomial_reg.yaml")

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray):
        try:
            X_train = np.nan_to_num(X_train, nan=-120, posinf=-120, neginf=-120)
            X_train = np.clip(X_train, -120, 0)

            # Scale input
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)

            # Polynomial transformation
            degree = self.config["degree"]
            include_bias = self.config["include_bias"]
            poly = PolynomialFeatures(degree=degree, include_bias=include_bias)
            X_poly = poly.fit_transform(X_train_scaled)

            # Fit linear model on polynomial features
            self.model = LinearRegression(fit_intercept=self.config["fit_intercept"])
            self.model.fit(X_poly, Y_train)

            # Store scalers and transformers as stateless config references
            self._scaler_mean = scaler.mean_
            self._scaler_scale = scaler.scale_
            self._poly_transformer = poly
        except Exception as e:
            logging.error(f"PolynomialRegressor fit failed: {e}")
            raise

    def predict(self, X_sample: np.ndarray) -> np.ndarray:
        try:
            X_sample = np.nan_to_num(X_sample, nan=-120, posinf=-120, neginf=-120)
            X_sample = np.clip(X_sample, -120, 0)
            X_sample = np.atleast_2d(X_sample)

            # Scale with stored stats
            X_sample_scaled = (X_sample - self._scaler_mean) / self._scaler_scale

            # Polynomial transform using fitted transformer
            X_sample_poly = self._poly_transformer.transform(X_sample_scaled)

            # Predict
            prediction = self.model.predict(X_sample_poly)
            return prediction[0] if X_sample.shape[0] == 1 else prediction
        except Exception as e:
            logging.error(f"PolynomialRegressor prediction failed: {e}")
            raise
