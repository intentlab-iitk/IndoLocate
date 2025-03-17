from sklearn.metrics import max_error, mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import math

def calculate_mae(Y_true, Y_pred):
    """
    Calculate Mean Absolute Error (MAE).
    
    Parameters:
    Y_true (array-like): Actual target values.
    Y_pred (array-like): Predicted target values.
    
    Returns:
    float: Mean Absolute Error
    """
    return mean_absolute_error(Y_true, Y_pred)

def calculate_mse(Y_true, Y_pred):
    """
    Calculate Mean Squared Error (MSE).
    
    Parameters:
    Y_true (array-like): Actual target values.
    Y_pred (array-like): Predicted target values.
    
    Returns:
    float: Mean Squared Error
    """
    return mean_squared_error(Y_true, Y_pred)

def calculate_rmse(Y_true, Y_pred):
    """
    Calculate Root Mean Squared Error (RMSE).
    
    Parameters:
    Y_true (array-like): Actual target values.
    Y_pred (array-like): Predicted target values.
    
    Returns:
    float: Root Mean Squared Error
    """
    mse = calculate_mse(Y_true, Y_pred)
    return mse ** 0.5

def calculate_r2(Y_true, Y_pred):
    """
    Calculate R² Score.
    
    Parameters:
    Y_true (array-like): Actual target values.
    Y_pred (array-like): Predicted target values.
    
    Returns:
    float: R² Score
    """
    return r2_score(Y_true, Y_pred)

def calculate_max_error(Y_true, Y_pred):
    """
    Calculate Max Error.
    
    Parameters:
    Y_true (array-like): Actual target values.
    Y_pred (array-like): Predicted target values.
    
    Returns:
    float: Max Error
    """
    return max_error(Y_true, Y_pred)

def calculate_mean_error(Y_true, Y_pred):
    """
    Calculate the localization error between true and predicted coordinates.

    Parameters:
    - Y_true: numpy array of shape (N, 3), true coordinates (x_true, y_true, z_true)
    - Y_pred: numpy array of shape (N, 3), predicted coordinates (x_pred, y_pred, z_pred)

    Returns:
    - mean_localization_error: float, average localization error across all points
    """
    # Validate input shapes
    if Y_true.shape != Y_pred.shape:
        raise ValueError("Y_true and Y_pred must have the same shape.")
    
    # Calculate mean localization error
    mean_localization_error = np.mean(np.sqrt(np.sum((Y_true - Y_pred) ** 2, axis=1)))
    
    return mean_localization_error

def calculate_median_error(true_pos, pred_pos):
    """
    Compute the median localization error.
    
    Parameters:
    - true_pos: numpy array of shape (N, 2) -> Ground truth (x, y) positions
    - pred_pos: numpy array of shape (N, 2) -> Predicted (x, y) positions
    
    Returns:
    - median_error: Median localization error
    """
    errors = np.linalg.norm(true_pos - pred_pos, axis=1)
    return np.median(errors)

def calculate_p80_error(true_pos, pred_pos):
    """
    Compute the 80th percentile localization error.
    
    Parameters:
    - true_pos: numpy array of shape (N, 2) -> Ground truth (x, y) positions
    - pred_pos: numpy array of shape (N, 2) -> Predicted (x, y) positions
    
    Returns:
    - p80_error: 80th percentile localization error
    """
    errors = np.linalg.norm(true_pos - pred_pos, axis=1)
    return np.percentile(errors, 80)