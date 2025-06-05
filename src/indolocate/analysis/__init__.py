"""
File            : indolocate/analysis/__init__.py   
Description     : Utilites module for indolocate package.
"""

# Imports
import logging
import numpy as np
import matplotlib.pyplot as plt

# Local imporrts
from .plots import (
    plot_metric,
    plot_histograms,
    plot_cdfs,
)
from .metrics import (
    calculate_mean, calculate_median, calculate_mode,
    calculate_stddev, calculate_minimum, calculate_maximum,
    calculate_mae, calculate_rmse, calculate_percetile
)

# Functions
def evaluate(true_positions: np.ndarray, predicted_positions: np.ndarray, algorithm_name: str) -> dict:

    errors = np.linalg.norm(true_positions - predicted_positions, axis=1)
    logging.info(f"Evaluation done for {algorithm_name}")
    return {
        "algorithm": algorithm_name,
        "errors": errors,
        "Mean": calculate_mean(errors),
        "Median": calculate_median(errors),
        "Mode": calculate_mode(errors),
        "StdDev": calculate_stddev(errors),
        "Min": calculate_minimum(errors),
        "Max": calculate_maximum(errors),
        "MAE": calculate_mae(errors),
        "RMSE": calculate_rmse(errors),
        "P80": calculate_percetile(errors, 80)
    }

def plot_metrics(metrics_list: list[dict]) -> None:
    """
    Visualizes metrics and distributions from a list of dictionaries.
    Each dictionary must include:
        - "algorithm": str
        - 9 metric fields (e.g., mean, median, stddev, etc.)
        - "errors": list or np.array of per-sample errors

    Produces:
        - 3x3 grid of bar charts for metric comparison
        - one figure with combined histograms and CDFs.
    """
    # Plots metrics
    metric_names = [key for key in metrics_list[0] if key not in ("algorithm", "errors")]
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle("Metrics", fontsize=20)

    axes = np.array(axes).flatten()

    for idx, metric_name in enumerate(metric_names):
        plot_metric(axes[idx], metrics_list, metric_name)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    # Plot histograms and CDFs
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle("Distributions", fontsize=16)

    plot_histograms(ax1, metrics_list)
    plot_cdfs(ax2, metrics_list)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def display_metrics(metrics_list: list[dict]) -> None:
    """
    Displays a neatly formatted metrics table in markdown style.
    Automatically extracts metric names from the input dictionaries.
    Each dictionary must include:
        - 'algorithm': str
        - 'errors': np.ndarray or list (optional)
        - other fields: any numeric metrics
    """
    if not metrics_list:
        print("No metrics to display.")
        return

    # Dynamically extract headers
    all_keys = metrics_list[0].keys()
    metric_keys = [k for k in all_keys if k not in ("algorithm", "errors")]
    headers = ["Algorithm"] + [k for k in metric_keys]

    # Build table rows
    rows = []
    for metrics in metrics_list:
        row = [metrics["algorithm"]] + [f"{metrics[k]:.4f}" for k in metric_keys]
        rows.append(row)

    # Calculate column widths
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*([headers] + rows))]
    format_row = lambda r: "| " + " | ".join(f"{cell:<{w}}" for cell, w in zip(r, col_widths)) + " |"

    # Print table
    print(format_row(headers))
    print("|" + "|".join("-" * (w + 2) for w in col_widths) + "|")
    for row in rows:
        print(format_row(row))


def display_locations(Y_true, Y_pred, name="Algorithm"):
    assert len(Y_true) == len(Y_pred), "Y_true and Y_pred must have the same length"
    total_samples = len(Y_true)
    dim = Y_true.shape[1]

    # Choose 4 starting indices, ensuring we have room for 5 continuous samples each
    np.random.seed(42)  # for reproducibility
    max_start = total_samples - 5
    starts = np.random.choice(max_start, size=4, replace=False)

    def format_coords(coords):
        return '(' + ', '.join(f'{x:6.2f}' for x in coords) + ')'

    print(f"\n{'=' * 30} {name} {'=' * 30}")
    print(f"{'Index':<6} | {'True Coordinates':<25} | {'Predicted Coordinates'}")
    print("-" * 70)
    for i, start in enumerate(starts, 1):
        for j in range(start, start + 5):
            true_coords = format_coords(Y_true[j])
            pred_coords = format_coords(Y_pred[j])
            print(f"{j:<6} | {true_coords:<25} | {pred_coords}")
    print("")

