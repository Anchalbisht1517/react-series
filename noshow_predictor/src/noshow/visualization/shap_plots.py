"""SHAP plot wrappers for the no-show predictor.

Provides helpers for Streamlit / notebook rendering of saved SHAP images.
"""

import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from noshow.config import project_config

OUTPUT_PLOT_DIR = os.path.join(project_config.ROOT_DIR, "outputs", "plots")


def get_shap_paths():
    """Return a dict of saved SHAP image paths."""
    return {
        "summary_bar": os.path.join(OUTPUT_PLOT_DIR, "shap_summary_bar.png"),
        "summary_dot": os.path.join(OUTPUT_PLOT_DIR, "shap_summary_dot.png"),
        "waterfall": os.path.join(OUTPUT_PLOT_DIR, "shap_waterfall.png"),
    }


def render_image(path: str, title: str = "", figsize=(10, 6)) -> Figure:
    """Load and display an image inside a matplotlib figure."""
    if not os.path.exists(path):
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, f"Image not found:\n{path}",
                ha="center", va="center", fontsize=12)
        ax.axis("off")
        return fig

    fig, ax = plt.subplots(figsize=figsize)
    img = plt.imread(path)
    ax.imshow(img)
    ax.axis("off")
    if title:
        ax.set_title(title)
    fig.tight_layout()
    return fig
