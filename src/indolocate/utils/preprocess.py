import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy.ndimage import uniform_filter1d

def preprocess_rssi(X_train,
                    Y_train,
                   smooth_window=1,
                   normalization=None,
                   clip_range=(-104, -5)):
    """
    Robust RSSI preprocessing pipeline with:
    - Missing value replacement with min clip value
    - Infinite value handling
    - Window-based smoothing
    - Value clipping
    - Optional normalization
    
    Parameters:
    - X_train: 2D numpy array (samples × N RSSI values)
    - window_size: smoothing window size (default: 5)
    - normalization: None, 'standard', or 'minmax' 
    - clip_range: Tuple of (min, max) values for clipping
    
    Returns:
    - Cleaned and processed RSSI data
    """
    
    data = np.array(X_train, dtype=np.float32)
    labels = Y_train
    min_clip, max_clip = clip_range
    
    # Handling data
    data = np.where(~np.isfinite(data), np.nan, data)
    data = np.where(np.isnan(data), min_clip, data)
    data = np.clip(data, min_clip, max_clip)
    
    # Apply smoothing
    if smooth_window > 1:
        data = uniform_filter1d(data, smooth_window, axis=0, mode='nearest')
    
    # Apply normalization
    if normalization == 'standard':
        data = StandardScaler().fit_transform(data)
    elif normalization == 'minmax':
        data = MinMaxScaler(feature_range=(0, 1)).fit_transform(data)
    
    return data, labels


def preprocess_csi(X_train, n=20):
    """
    Reduces CSI from a single AP using magnitude + phase and PCA.
    
    Parameters:
        X_train (ndarray): Complex CSI of shape (samples, carriers, antennas) for a single AP
        n_components (int): Number of PCA components

    Returns:
        np.ndarray: Reduced CSI X_train of shape (samples, n_components)
    """
    n_samples = X_train.shape[0]

    X_mag = np.abs(X_train)
    X_phase = np.angle(X_train)

    X_combined = np.concatenate([X_mag, X_phase], axis=-1)

    # Flatten to (samples, X_train)
    X_flat = X_combined.reshape(n_samples, -1)

    # PCA
    pca = PCA(n_components=n)
    X_csi_reduced = pca.fit_transform(X_flat)

    return X_csi_reduced
