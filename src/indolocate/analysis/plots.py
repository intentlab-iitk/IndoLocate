import numpy as np
from matplotlib.axes import Axes

def plot_metric(ax: Axes, metrics_list, metric_name):
    """
    Plots a single metric across algorithms into the given axis with legend.
    """
    algos = [m["algorithm"] for m in metrics_list]
    values = [m[metric_name] for m in metrics_list]
    
    ax.bar(algos, values)

    ax.set_title(metric_name)
    ax.set_ylabel("Error (m)")
    ax.set_xlabel("Algorithm")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

def plot_histograms(ax: Axes, metrics_list):
    """
    Plots outline-only histogram for multiple algorithms in the same subplot.
    """
    for m in metrics_list:
        errors = np.array(m["errors"])
        counts, bin_edges = np.histogram(errors, bins=30)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        ax.plot(bin_centers, counts, label=m["algorithm"], linewidth=2)
    
    ax.set_title("Histograms")
    ax.set_xlabel("Error (m)")
    ax.set_ylabel("Frequency")
    ax.legend()
    ax.grid(True)

def plot_cdfs(ax: Axes, metrics_list):
    """
    Plots CDFs for all algorithms in the same subplot.
    """
    for m in metrics_list:
        errors = np.sort(np.array(m["errors"]))
        cdf = np.arange(len(errors)) / len(errors)
        ax.plot(errors, cdf, label=m["algorithm"], linewidth=2)

    ax.set_title("CDFs")
    ax.set_xlabel("Error (m)")
    ax.set_ylabel("CDF")
    ax.legend()
    ax.grid(True)
