import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler

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

def preprocess_csi(csi_data: np.ndarray, use_phase=True, normalize=True, pca_components=None):
    """
    Preprocess CSI data for kNN by extracting real values, flattening, and normalizing.

    Parameters:
    csi_data (numpy.ndarray): CSI data of shape (samples, subcarriers, antennas, APs) with complex values.
    use_phase (bool): Whether to include phase information along with magnitude.
    normalize (bool): Whether to normalize data using standardization.
    pca_components (int or None): If not None, applies PCA to reduce dimensions.

    Returns:
    np.ndarray: Processed CSI features (samples, features).
    """
    num_samples = csi_data.shape[0]

    # Extract magnitude and phase
    magnitude = np.abs(csi_data)  # Shape: (samples, subcarriers, antennas, APs)
    phase = np.angle(csi_data)    # Shape: (samples, subcarriers, antennas, APs)

    # Concatenate magnitude and phase if required
    if use_phase:
        csi_features = np.concatenate([magnitude, phase], axis=1)  # Shape: (samples, 2*subcarriers, antennas, APs)
    else:
        csi_features = magnitude  # Only magnitude

    # Flatten CSI features to 2D (samples, features)
    csi_features = csi_features.reshape(num_samples, -1)

    # Normalize data
    if normalize:
        scaler = StandardScaler()  # Standardization (zero mean, unit variance)
        csi_features = scaler.fit_transform(csi_features)

    # Apply PCA for dimensionality reduction if specified
    if pca_components:
        pca = PCA(n_components=pca_components)
        csi_features = pca.fit_transform(csi_features)

    return csi_features
