"""
File            : indolocate/algorithms/__init__.py  
Description     : Init file for algorithms module.  
"""

# Imports
import logging
from typing import Literal, get_args
from .base import Algorithm

ALGORITHM = Literal[
    "BaseModel",
    "kNNRegressor",
    "LinearRegressor",
    "RidgeRegressor",
    "LassoRegressor",
    "PolynomialRegressor",
]

# Dynamically extract valid algorithm names from Literal
VALID_ALGORITHMS = get_args(ALGORITHM)

def init(algorithm_name: ALGORITHM) -> Algorithm:
    if algorithm_name == "BaseModel":
        return Algorithm()
    elif algorithm_name == "kNNRegressor":
        from .knn import kNNRegressor
        return kNNRegressor()
    elif algorithm_name == "LinearRegressor":
        from .linear import LinearRegressor
        return LinearRegressor()
    elif algorithm_name == "RidgeRegressor":
        from .linear import RidgeRegressor
        return RidgeRegressor()
    elif algorithm_name == "LassoRegressor":
        from .linear import LassoRegressor
        return LassoRegressor()
    elif algorithm_name == "PolynomialRegressor":
        from .nonlinear import PolynomialRegressor
        return PolynomialRegressor()
    else:
        logging.error(
            f"Unknown algorithm: {repr(algorithm_name)}. "
            f"Valid options: {', '.join(get_args(ALGORITHM))}"
        )
        raise SystemExit("Invalid algorithm provided.")

