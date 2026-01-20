import os
import matplotlib.pyplot as plt

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_plot(filename, folder="results"):
    ensure_dir(folder)
    path = os.path.join(folder, filename)
    plt.savefig(path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {path}")



