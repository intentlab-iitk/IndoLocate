# indolocate/__init__.py
"""
Indolocate: A package for implementing indoor localization techniques.
"""
__version__ = "0.1.0"

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from .algorithms import *
from .utils import *

def create_model(algorithm, file_config=None):
    """
    Creates a model with the given configuration file.

    Parameters:
        algorithm   : The algorithm class (e.g., DNN, KNN).
        config      : Configuration dictionary for the model.
    
    Returns:
        An instance of the specified model.
    """
    if algorithm == "knn":
        return kNNRegression(file_config)
    elif algorithm == "rf":
        return RFRegression(file_config)
    elif algorithm == "dnn":
        return DNNRegression(file_config)
    elif algorithm == "gbdt":
        return GBDTRegression(file_config)
    elif algorithm == "lstm":
        return LSTMRegression(file_config)
    else:
        print("Invalid algorithm")
