"""Model training component for the no-show predictor.

Trains four models in comparison order:
  1. LogisticRegression (baseline)
  2. DecisionTreeClassifier
  3. RandomForestClassifier
  4. XGBClassifier (primary)

Saves the best model to ``models/xgboost_model_v2.pkl``.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config
from noshow.utils import load_object, save_object

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Model registry & factory
# ---------------------------------------------------------------------------

_MODEL_REGISTRY = {
    "logistic_regression": LogisticRegression,
    "decision_tree": DecisionTreeClassifier,
    "random_forest": RandomForestClassifier,
}


def _build_xgboost(params: dict):
    """Lazy import XGBoost so the pipeline does not hard-fail if xgboost
    is not installed during component import."""
    try:
        from xgboost import XGBClassifier
    except ImportError as exc:
        raise NoShowException(
            "xgboost is required but not installed. Run: pip install xgboost"
        ) from exc
    return XGBClassifier(**params)


# ---------------------------------------------------------------------------
# Trainer class
# ---------------------------------------------------------------------------

class ModelTrainer:
    """
    Loads the transformed artifacts produced in Phase 2,
    fits each model, evaluates on the held-out test set,
    and persists the primary (XGBoost) model.
    """

    def __init__(self):
        self.artifacts_dir = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("artifacts_root", "artifacts"),
            "data_transformation"
        )
        self.models_dir = os.path.join(project_config.ROOT_DIR, "models")
        self.outputs_dir = os.path.join(project_config.ROOT_DIR, "outputs")
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.outputs_dir, exist_ok=True)

        self.params = project_config.params

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_artifacts(self):
        """Load train/test splits and resampled training data."""
        try:
            X_train = load_object(os.path.join(self.artifacts_dir, "X_train.pkl"))
            X_test = load_object(os.path.join(self.artifacts_dir, "X_test.pkl"))
            y_train = load_object(os.path.join(self.artifacts_dir, "y_train.pkl"))
            y_test = load_object(os.path.join(self.artifacts_dir, "y_test.pkl"))
            X_train_res = load_object(os.path.join(self.artifacts_dir, "X_train_resampled.pkl"))
            y_train_res = load_object(os.path.join(self.artifacts_dir, "y_train_resampled.pkl"))
            logger.info("Transformation artifacts loaded successfully.")
            return X_train, X_test, y_train, y_test, X_train_res, y_train_res
        except Exception as e:
            logger.error(f"Failed to load transformation artifacts: {e}")
            raise NoShowException("Artifact loading failed", sys.exc_info()) from e

    # ------------------------------------------------------------------
    # Model builders
    # ------------------------------------------------------------------

    def _build_lr(self):
        cfg = self.params.get("model", {}).get("logistic_regression", {})
        return LogisticRegression(**cfg)

    def _build_dt(self):
        cfg = self.params.get("model", {}).get("decision_tree", {})
        return DecisionTreeClassifier(**cfg)

    def _build_rf(self):
        cfg = self.params.get("model", {}).get("random_forest", {})
        return RandomForestClassifier(**cfg)

    def _build_xgb(self):
        cfg = self.params.get("model", {}).get("xgboost", {})
        return _build_xgboost(cfg)

    # ------------------------------------------------------------------
    # Training & evaluation
    # ------------------------------------------------------------------

    def train_and_evaluate(self, model, model_name: str,
                           X_train, y_train, X_test, y_test):
        logger.info(f"Training {model_name} ...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        metrics = {
            "model": model_name,
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision": round(precision_score(y_test, y_pred), 4),
            "recall": round(recall_score(y_test, y_pred), 4),
            "f1": round(f1_score(y_test, y_pred), 4),
            "roc_auc": round(roc_auc_score(y_test, y_prob), 4),
        }
        logger.info(f"{model_name} metrics: {metrics}")
        return model, metrics

    # ------------------------------------------------------------------
    # Orchestrator
    # ------------------------------------------------------------------

    def initiate_model_training(self):
        try:
            (
                X_train, X_test, y_train, y_test,
                X_train_res, y_train_res,
            ) = self.load_artifacts()

            results = []

            # 1. Logistic Regression (baseline) — fit on original train
            lr = self._build_lr()
            _, lr_metrics = self.train_and_evaluate(lr, "LogisticRegression",
                                                     X_train, y_train,
                                                     X_test, y_test)
            results.append(lr_metrics)

            # 2. Decision Tree — fit on original train
            dt = self._build_dt()
            _, dt_metrics = self.train_and_evaluate(dt, "DecisionTree",
                                                       X_train, y_train,
                                                       X_test, y_test)
            results.append(dt_metrics)

            # 3. Random Forest — fit on original train
            rf = self._build_rf()
            _, rf_metrics = self.train_and_evaluate(rf, "RandomForest",
                                                     X_train, y_train,
                                                     X_test, y_test)
            results.append(rf_metrics)

            # 4. XGBoost (primary) — fit on SMOTE-resampled train
            xgb = self._build_xgb()
            _, xgb_metrics = self.train_and_evaluate(xgb, "XGBoost",
                                                        X_train_res, y_train_res,
                                                        X_test, y_test)
            results.append(xgb_metrics)

            # Save primary model
            xgb_path = os.path.join(self.models_dir, "xgboost_model_v2.pkl")
            save_object(xgb_path, xgb)
            logger.info(f"Primary XGBoost model saved to {xgb_path}")

            # Save comparison CSV
            comparison_df = pd.DataFrame(results)
            comparison_path = os.path.join(self.outputs_dir, "model_comparison.csv")
            comparison_df.to_csv(comparison_path, index=False)
            logger.info(f"Model comparison saved to {comparison_path}")

            # Save trainer artifacts
            trainer_artifact_dir = os.path.join(
                project_config.ROOT_DIR,
                project_config.config.get("artifacts_root", "artifacts"),
                "model_trainer"
            )
            os.makedirs(trainer_artifact_dir, exist_ok=True)
            save_object(os.path.join(trainer_artifact_dir, "all_models.pkl"),
                        {"lr": lr, "dt": dt, "rf": rf, "xgb": xgb})

            logger.info("Model training pipeline completed successfully.")
            return xgb, comparison_df

        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise NoShowException("Model training failed", sys.exc_info()) from e


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.initiate_model_training()
