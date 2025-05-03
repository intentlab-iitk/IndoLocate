# Project       : indolocate
# File          : locator.py

# Imports
import numpy as np
from IPython.display import HTML
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Functions
def locator(IP="127.0.0.1", Port=9000):
    finder = Locator()
    finder.configure(IP, Port)
    finder.secrect(None)
    return finder

class Locator:
    def __init__(self):
        self.ip = None
        self.port = None
        self.password = None

    def configure(self, IP, Port):
        self.ip = IP
        self.port = Port

    def secrect(self, Password):
        self.password = Password


    def animate(self, locations: np.ndarray, save_path: str = None):
        fig, ax = plt.subplots()
        ax.set_xlim(np.min(locations[:, 0]) - 1, np.max(locations[:, 0]) + 1)
        ax.set_ylim(np.min(locations[:, 1]) - 1, np.max(locations[:, 1]) + 1)
        path, = ax.plot([], [], 'b-', lw=2)
        dot, = ax.plot([], [], 'ro')

        def init():
            path.set_data([], [])
            dot.set_data([], [])
            return path, dot

        def update(i):
            path.set_data(locations[:i+1, 0], locations[:i+1, 1])
            dot.set_data([locations[i, 0]], [locations[i, 1]])  # <-- fix for single point
            return path, dot

        self.anim = FuncAnimation(
            fig, update, frames=len(locations),
            init_func=init, blit=True, interval=300, repeat=False
        )

        if save_path:
            self.anim.save(save_path, writer='ffmpeg', fps=30)  # Save as .mp4 by default

        return HTML(self.anim.to_jshtml())

    def run(self):
        pass
