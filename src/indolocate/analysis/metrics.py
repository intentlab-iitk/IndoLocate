import statistics as stats
import numpy as np

def calculate_errors(true_positions: np.ndarray, predicted_positions: np.ndarray) -> np.ndarray:
    """
    Calculate the Euclidean distance errors between true and predicted positions.

    Args:
        true_positions (np.ndarray): Array of true position coordinates with shape (N, D),
        predicted_positions (np.ndarray): Array of predicted position coordinates with shape (N, D).

    Returns:
        np.ndarray: A 1D array containing the Euclidean distance error for each sample.
    """
    return np.linalg.norm(true_positions - predicted_positions, axis=1)

def calculate_mean(errors: np.ndarray) -> float:
    """
    Calculate the arithmetic mean (average) of a list of errors.

    Args:
        errors (list of float): A list containing error values.

    Returns:
        float: The mean of the error values.
    """
    return stats.mean(errors)

def calculate_median(errors: np.ndarray) -> float:
    """
    Calculate the median value from a list of errors.

    Args:
        errors (list of float): A list containing error values.

    Returns:
        float: The median error value.
    """
    return stats.median(errors)

def calculate_mode(errors: np.ndarray) -> float:
    """
    Calculate the mode (most frequent value) from a list of errors.

    Args:
        errors (list of float): A list containing error values.

    Returns:
        float: The mode of the error values.
    
    Raises:
        statistics.StatisticsError: If no unique mode exists.
    """
    return stats.mode(errors)

def calculate_stddev(errors: np.ndarray) -> float:
    """
    Calculate the population standard deviation of error values.

    Args:
        errors (list of float): A list containing error values.

    Returns:
        float: The standard deviation of the errors.
    """
    return stats.pstdev(errors)

def calculate_minimum(errors: np.ndarray) -> float:
    """
    Retrieve the minimum (smallest) error value from the list.

    Args:
        errors (list of float): A list containing error values.

    Returns:
        float: The minimum error value.
    """
    return np.min(errors)

def calculate_maximum(errors: np.ndarray) -> float:
    """
    Retrieve the maximum (largest) error value from the list.

    Args:
        errors (list of float): A list containing error values.

    Returns:
        float: The maximum error value.
    """
    return np.max(errors)

def calculate_mae(errors: np.ndarray) -> float:
    """
    Calculate the Mean Absolute Error (MAE) from a list of errors.

    Args:
        errors (list of float): A list containing error values.

    Returns:
        float: The mean of the absolute error values.
    """
    return np.mean(np.abs(errors))

def calculate_rmse(errors: np.ndarray) -> float:
    """
    Calculate the Root Mean Square Error (RMSE) from a list of errors.

    Args:
        errors (list of float): A list containing error values.

    Returns:
        float: The root mean square error value.
    """
    return np.sqrt(np.mean(np.square(errors)))

def calculate_percetile(errors: np.ndarray, n: int) -> float:
    """
    Calculate the nth percentile of error values.

    Args:
        errors (list of float): A list containing error values.
        n (int): The desired percentile (between 0 and 100).

    Returns:
        float: The value at the nth percentile.
    """
    return np.percentile(errors, n)
