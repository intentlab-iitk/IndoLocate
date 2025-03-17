import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess_rssi(X_train: np.ndarray, Y_train, normalize=True):
    """
    Preprocess RSSI data:
    1. Replace RSSI = 100 (no signal) with -104.
    2. Normalize the data using Min-Max scaling between -104 and 0 dBm.
    3. Remove outliers row-wise using Z-score method if specified.
    
    Parameters:
    - data (np.ndarray): The input RSSI data (rows are samples, columns are APs).
    - normalize (bool): Whether to normalize the data using Min-Max scaling.
    - remove_outliers (bool): Whether to remove outliers using Z-score method.
    - z_threshold (float): The Z-score threshold to define outliers.
    
    Returns:
    - preprocessed_data (np.ndarray): The processed RSSI data.
    """
    
    X_train = X_train.astype(float)  # Ensure the data is of float type to handle operations
    X_train[X_train >= -35] = -104  # Replace RSSI = 100 (no signal) with -104
    X_train[X_train <= -104] = -104  # Replace RSSI = 100 (no signal) with -104
    
    # Step 2: Normalize the data using Min-Max scaling (if required)
    if normalize:
        scaler = MinMaxScaler(feature_range=(0, 1))  # Scale to [0, 1]
        X_train = scaler.fit_transform(X_train)
    
    return X_train, Y_train
