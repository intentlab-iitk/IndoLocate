from .base import Algorithm

def init(alogrithm: str)-> Algorithm:
    """
    This function loads and returns an initialized instance of that algorithm.

    Parameters:
        algorithm (str): The name of the algorithm to load (e.g., "knn", "svm").

    Returns:
        Instance (class): An instance of the corresponding algorithm class.

    Raises:
        ValueError: If the given algorithm name is not supported.
    """
    algo_map = {
        "knn": lambda: __import__(__name__ + '.knn', fromlist=['kNN']).kNN(),
        "svm": lambda: __import__(__name__ + '.svm', fromlist=['SVM']).SVM(),
    }

    key = alogrithm.lower()
    try:
        return algo_map[key]()
    except KeyError:
        raise ValueError(f"Unknown model: {alogrithm}")
