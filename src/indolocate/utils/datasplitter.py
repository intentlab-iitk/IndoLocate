from sklearn.model_selection import train_test_split

def get_trainset(features, labels, test_size=0.2, random_state=42):
    """
    Returns only the training set after splitting.

    Parameters:
    - features (np.array): Feature matrix (samples, features)
    - labels (np.array): Label matrix (samples, labels)
    - test_size (float): Fraction of data to be used as test set (default: 0.2)
    - random_state (int): Seed for reproducibility (default: 42)

    Returns:
    - X_train (np.array): Training features
    - Y_train (np.array): Training labels
    """
    X_train, _, Y_train, _ = train_test_split(
        features, labels, test_size=test_size, random_state=random_state
    )
    return X_train, Y_train

def get_testset(features, labels, test_size=0.2, random_state=42):
    """
    Returns only the testing set after splitting.

    Parameters:
    - features (np.array): Feature matrix (samples, features)
    - labels (np.array): Label matrix (samples, labels)
    - test_size (float): Fraction of data to be used as test set (default: 0.2)
    - random_state (int): Seed for reproducibility (default: 42)

    Returns:
    - X_test (np.array): Testing features
    - Y_test (np.array): Testing labels
    """
    _, X_test, _, Y_test = train_test_split(
        features, labels, test_size=test_size, random_state=random_state
    )
    return X_test, Y_test