import matplotlib.pyplot as plt
from .metrics import *

def evaluate_model(model, X_test, Y_test):
    """
    Evaluate the performance of a trained localization model on test data.

    Parameters:
    model: Trained regression model
    X_test (numpy.ndarray or pandas.DataFrame): Features for testing
    Y_test (numpy.ndarray or pandas.DataFrame): True target values for testing

    Returns:
    dict: Evaluation metrics including MAE, RMSE, and R² Score
    """
    # Predict using the model
    Y_pred = model.predict(X_test)
    
    # Calculate evaluation metrics using individual functions
    mae = calculate_mae(Y_test, Y_pred)
    rmse = calculate_rmse(Y_test, Y_pred)
    le = calculate_mean_error(Y_test, Y_pred)
    r2 = calculate_r2(Y_test, Y_pred)


    # Create a dictionary of metrics
    metrics = {
        "Algorithm": model.name,
        "Mean Absolute Error (MAE)": mae,
        "Root Mean Squared Error (RMSE)": rmse,
        "Localization Error (LE)": le,
        "R-squared (R²)": r2,
    }

    # Print the metrics
    for key, value in metrics.items():
        print(f"[metrics] {key}: {value}")
    
    return metrics

def plot_metrics(metrics_list):
    """
    Plots each metric in a separate figure.

    Parameters:
    - metrics_list: List of dictionaries containing metrics. Each dictionary should include an 'Algorithm' key.
    - title: Overall title text to append to each subplot's title.
    - cmap: Name of the matplotlib colormap to use for assigning colors.
    """
    # Extract metric names from the first dictionary (excluding "Algorithm")
    title = ""
    cmap = 'viridis'
    metrics = list(metrics_list[0].keys())
    if 'Algorithm' in metrics:
        metrics.remove('Algorithm')
    
    # Extract model names from the 'Algorithm' key
    model_names = [d['Algorithm'] for d in metrics_list]
    
    # Create a colormap instance with as many distinct colors as there are models
    cmap_instance = plt.cm.get_cmap(cmap, len(model_names))
    colors = [cmap_instance(i) for i in range(len(model_names))]
    
    # Loop through each metric and create a separate figure for it
    for metric_name in metrics:
        # Create a new figure and axis for each metric
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract values for the current metric from all models
        values = [d[metric_name] for d in metrics_list]
        
        # Create the bar plot with assigned colors
        bars = ax.bar(model_names, values, color=colors)
        
        # Set title (appending the provided overall title if given), and labels
        ax.set_title(f"{metric_name} {('- ' + title) if title else ''}")
        ax.set_xlabel('Models')
        ax.set_ylabel('Error')
        
        # Annotate each bar with its corresponding value
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', 
                    ha='center', va='bottom')
        
        # Improve layout spacing
        plt.tight_layout()
        plt.show()

def evaluate_location(true_pos: np.ndarray, pred_pos: np.ndarray):
    """
    Function to evaluate the localization algorithm.

    Parameters:
    true_pos (ndarray): True location coordinates.
    pred_pos (ndarray): Predicted location coordinates.
    """
    median_error = calculate_median_error(true_pos, pred_pos)
    p80_error = calculate_p80_error(true_pos, pred_pos)

    print(f"[#] Median Localization Error: {median_error:.2f} m")
    print(f"[#] P-80th Localization Error: {p80_error:.2f} m")