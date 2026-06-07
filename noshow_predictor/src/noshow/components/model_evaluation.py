"""Model evaluation component.

Loads the four trained models, evaluates each on the held-out test set,
and persists confusion-matrix images plus an enriched comparison CSV.
"""

import os
import sys
import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
)

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config
from noshow.utils import load_object, ensure_dir

logger = get_logger(__name__)

PLOT_DIR = os.path.join(project_config.ROOT_DIR, "outputs", "plots")
os.makedirs(PLOT_DIR, exist_ok=True)


class ModelEvaluation:
    """
    Orchestrates post-training evaluation for all saved models.
    """

    def __init__(self):
        self.artifacts_dir = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("artifacts_root", "artifacts"),
            "data_transformation"
        )
        self.trainer_dir = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("artifacts_root", "artifacts"),
            "model_trainer"
        )
        self.outputs_dir = os.path.join(project_config.ROOT_DIR, "outputs")
        ensure_dir(self.outputs_dir)
        ensure_dir(PLOT_DIR)

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_test_data(self):
        X_test = load_object(os.path.join(self.artifacts_dir, "X_test.pkl"))
        y_test = load_object(os.path.join(self.artifacts_dir, "y_test.pkl"))
        return X_test, y_test

    def _load_models(self):
        models_path = os.path.join(self.trainer_dir, "all_models.pkl")
        models = load_object(models_path)
        logger.info(f"Loaded models: {list(models.keys())}")
        return models

    # ------------------------------------------------------------------
    # Metric computation
    # ------------------------------------------------------------------

    def _compute_metrics(self, y_true, y_pred, y_prob):
        return {
            "accuracy": round(accuracy_score(y_true, y_pred), 4),
            "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
            "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
            "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
            "roc_auc": round(roc_auc_score(y_true, y_prob), 4),
        }

    # ------------------------------------------------------------------
    # Plot helpers (matplotlib only — no seaborn required)
    # ------------------------------------------------------------------

    def _plot_confusion_matrix(self, cm, model_name):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)
        classes = ["Attended (0)", "No-Show (1)"]
        ax.set(
            xticks=np.arange(cm.shape[1]),
            yticks=np.arange(cm.shape[0]),
            xticklabels=classes,
            yticklabels=classes,
            title=f"Confusion Matrix — {model_name}",
            ylabel="True label",
            xlabel="Predicted label",
        )
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        thresh = cm.max() / 2.0
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], ","),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        fig.tight_layout()
        out = os.path.join(PLOT_DIR, f"confusion_matrix_{model_name.lower().replace(' ', '_')}.png")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        logger.info(f"Saved confusion matrix: {out}")
        plt.close(fig)

    def _plot_roc_curves(self, roc_data):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 6))
        for model_name, (fpr, tpr, auc) in roc_data.items():
            ax.plot(fpr, tpr, label=f"{model_name} (AUC = {auc:.3f})")
        ax.plot([0, 1], [0, 1], "k--", lw=1)
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curves")
        ax.legend(loc="lower right")
        fig.tight_layout()
        out = os.path.join(PLOT_DIR, "roc_curve.png")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        logger.info(f"Saved ROC curves: {out}")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Orchestrator
    # ------------------------------------------------------------------

    def initiate_model_evaluation(self):
        try:
            X_test, y_test = self._load_test_data()
            models = self._load_models()

            records = []
            roc_data = {}

            for name, model in models.items():
                y_pred = model.predict(X_test)
                y_prob = model.predict_proba(X_test)[:, 1]

                cm = confusion_matrix(y_test, y_pred)
                self._plot_confusion_matrix(cm, name)

                metrics = self._compute_metrics(y_test, y_pred, y_prob)
                metrics["model"] = name
                records.append(metrics)

                fpr, tpr, _ = roc_curve(y_test, y_prob)
                roc_data[name] = (fpr, tpr, metrics["roc_auc"])

            self._plot_roc_curves(roc_data)

            # Save / overwrite comparison CSV
            comparison_df = pd.DataFrame(records)
            comparison_path = os.path.join(self.outputs_dir, "model_comparison.csv")
            comparison_df.to_csv(comparison_path, index=False)
            logger.info(f"Updated model comparison CSV: {comparison_path}")

            # Recall is the primary metric
            best_recall = comparison_df.loc[comparison_df["recall"].idxmax()]
            logger.info(f"Best recall: {best_recall['model']} = {best_recall['recall']}")

            logger.info("Model evaluation completed successfully.")
            return comparison_df

        except Exception as e:
            logger.error(f"Model evaluation failed: {e}")
            raise NoShowException("Model evaluation failed", sys.exc_info()) from e


if __name__ == "__main__":
    evaluator = ModelEvaluation()
    evaluator.initiate_model_evaluation()
