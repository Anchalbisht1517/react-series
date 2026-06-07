"""SHAP explainability component for the no-show predictor.

Generates global summary plots (bar + dot) and a per-patient waterfall
using the saved XGBoost model.
"""

import os
import sys
import numpy as np
import pandas as pd

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config
from noshow.utils import load_object, ensure_dir

logger = get_logger(__name__)

PLOT_DIR = os.path.join(project_config.ROOT_DIR, "outputs", "plots")
ensure_dir(PLOT_DIR)


class Explainability:
    """
    Wraps SHAP explainers and plot generation for the primary XGBoost model.
    """

    def __init__(self):
        self.models_dir = os.path.join(project_config.ROOT_DIR, "models")
        self.artifacts_dir = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("artifacts_root", "artifacts"),
            "data_transformation"
        )
        self.outputs_dir = os.path.join(project_config.ROOT_DIR, "outputs")
        ensure_dir(PLOT_DIR)

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_model_and_data(self):
        model_path = os.path.join(self.models_dir, "xgboost_model_v2.pkl")
        if not os.path.exists(model_path):
            raise NoShowException(f"Model not found at {model_path}. Train first.")
        model = load_object(model_path)

        X_train = load_object(os.path.join(self.artifacts_dir, "X_train.pkl"))
        # Sample background for SHAP efficiency
        background = X_train.sample(n=min(100, len(X_train)), random_state=42)
        return model, background

    # ------------------------------------------------------------------
    # SHAP plot generation
    # ------------------------------------------------------------------

    def generate_shap_plots(self):
        try:
            import shap
            import matplotlib.pyplot as plt
        except ImportError as exc:
            raise NoShowException(
                "shap is required but not installed. Run: pip install shap"
            ) from exc

        model, background = self._load_model_and_data()
        logger.info("Building SHAP TreeExplainer ...")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(background)

        # Handle binary classification shape (list of two arrays)
        if isinstance(shap_values, list):
            sv = shap_values[1]  # class 1 (no-show)
            base_value = explainer.expected_value[1] if hasattr(explainer.expected_value, "__len__") else explainer.expected_value
        else:
            sv = shap_values
            base_value = explainer.expected_value

        # 1. Summary bar (global feature importance)
        fig, ax = plt.subplots(figsize=(10, 8))
        shap.summary_plot(sv, background, plot_type="bar", show=False)
        fig.tight_layout()
        out_bar = os.path.join(PLOT_DIR, "shap_summary_bar.png")
        fig.savefig(out_bar, dpi=150, bbox_inches="tight")
        logger.info(f"Saved SHAP summary bar: {out_bar}")
        plt.close(fig)

        # 2. Summary dot (direction + magnitude per feature)
        fig, ax = plt.subplots(figsize=(10, 8))
        shap.summary_plot(sv, background, show=False)
        fig.tight_layout()
        out_dot = os.path.join(PLOT_DIR, "shap_summary_dot.png")
        fig.savefig(out_dot, dpi=150, bbox_inches="tight")
        logger.info(f"Saved SHAP summary dot: {out_dot}")
        plt.close(fig)

        # 3. Waterfall for a single patient (first sample)
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.waterfall_plot(
            shap.Explanation(
                values=sv[0],
                base_values=base_value,
                data=background.iloc[0].values,
                feature_names=background.columns.tolist(),
            ),
            show=False,
        )
        fig.tight_layout()
        out_water = os.path.join(PLOT_DIR, "shap_waterfall.png")
        fig.savefig(out_water, dpi=150, bbox_inches="tight")
        logger.info(f"Saved SHAP waterfall: {out_water}")
        plt.close(fig)

        logger.info("SHAP explainability pipeline completed successfully.")

    def initiate_explainability(self):
        self.generate_shap_plots()


if __name__ == "__main__":
    exp = Explainability()
    exp.initiate_explainability()
