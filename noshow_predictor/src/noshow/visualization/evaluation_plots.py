"""Evaluation plot wrappers for the no-show predictor.

These functions are thin utilities that can be imported by notebooks or
Streamlit pages to render saved evaluation images.
"""

import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from noshow.config import project_config

OUTPUT_PLOT_DIR = os.path.join(project_config.ROOT_DIR, "outputs", "plots")


def get_confusion_matrix_path(model_name: str = "xgboost") -> str:
    """Return the saved confusion matrix image path for a given model."""
    fname = f"confusion_matrix_{model_name.lower().replace(' ', '_')}.png"
    return os.path.join(OUTPUT_PLOT_DIR, fname)


def get_roc_curve_path() -> str:
    """Return the saved ROC curve image path."""
    return os.path.join(OUTPUT_PLOT_DIR, "roc_curve.png")


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
