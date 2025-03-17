class SVMRegression:
    def __init__(self, file_config=None):
        """
        Initialize the KNN Regression model.

        Parameters:
        config_path (str): Path to the YAML configuration file. If None, default settings are used.
        """
        default_config = {
        'n_neighbours': 5
        }
        print(self.config)
        self.K = 5