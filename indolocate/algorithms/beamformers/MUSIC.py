import numpy as np
import matplotlib.pyplot as plt

def apply_MUSIC(X, antenna_spacing, central_freq, num_sources):
    """
    Estimate the Angle of Arrival (AoA) using the MUSIC algorithm.

    Parameters:
        X (numpy.ndarray): CSI matrix of dimensions M x N (M antennas, N subcarriers).
        antenna_spacing (float): Distance between adjacent antennas (in meters).
        central_freq (float): Central frequency of the signal (in Hz).
        num_sources (int): Number of signal sources (D).

    Returns:
        numpy.ndarray: Estimated AoA(s) in degrees.
        numpy.ndarray: MUSIC spectrum for visualization.
    """
    # Constants
    c = 3e8  # Speed of light in meters/second
    wavelength = c / central_freq  # Calculate wavelength

    # Internal angle grid
    angle_grid = np.linspace(-90, 90, 180)  # Angle grid for AoA search (in degrees)

    M, N = X.shape  # M: number of antennas, N: number of subcarriers

    # Step 1: Compute the spatial covariance matrix
    R = np.zeros((M, M), dtype=complex)
    for n in range(N):
        R += np.outer(X[:, n], X[:, n].conj())
    R /= N

    # Step 2: Eigenvalue decomposition
    eigenvalues, eigenvectors = np.linalg.eig(R)
    sorted_indices = np.argsort(eigenvalues)[::-1]  # Sort in descending order
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # Step 3: Separate signal and noise subspaces
    noise_subspace = eigenvectors[:, num_sources:]  # Noise subspace eigenvectors

    # Step 4: Compute the MUSIC spectrum
    music_spectrum = np.zeros_like(angle_grid, dtype=float)
    for i, theta in enumerate(angle_grid):
        steering_vector = np.exp(-1j * 2 * np.pi * antenna_spacing / wavelength * np.sin(np.deg2rad(theta)) * np.arange(M))
        steering_vector = steering_vector.reshape(-1, 1)
        music_spectrum[i] = 1 / np.abs((steering_vector.conj().T @ noise_subspace @ noise_subspace.conj().T @ steering_vector).item())

    # Step 5: Find peaks in the MUSIC spectrum
    peak_indices = np.argsort(music_spectrum)[-num_sources:]  # Indices of the largest peaks
    estimated_aoa = angle_grid[peak_indices]

    return estimated_aoa, music_spectrum
