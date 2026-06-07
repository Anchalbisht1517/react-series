"""Prediction pipeline for the no-show predictor.

Accepts raw patient dictionaries or batch DataFrames, applies the saved
preprocessor and XGBoost model, and returns a no-show probability with
an actionable risk tier.
"""

import os
import sys
import json
import pandas as pd
import numpy as np

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config
from noshow.utils import load_object

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Risk thresholds (loaded from params.yaml, with safe defaults)
# ---------------------------------------------------------------------------
_params = project_config.params.get("prediction", {})
HIGH_THRESHOLD = _params.get("high_risk_threshold", 0.65)
MEDIUM_THRESHOLD = _params.get("medium_risk_threshold", 0.40)


def _map_risk(probability: float) -> dict:
    """
    Map a no-show probability to a risk tier and recommended action.

    Parameters
    ----------
    probability : float
        Model output from ``predict_proba`` (class 1).

    Returns
    -------
    dict
        {"tier": str, "action": str, "probability": float}
    """
    if probability > HIGH_THRESHOLD:
        tier = "High"
        action = "Call + SMS reminder"
    elif probability >= MEDIUM_THRESHOLD:
        tier = "Medium"
        action = "SMS reminder"
    else:
        tier = "Low"
        action = "Standard appointment"
    return {
        "tier": tier,
        "action": action,
        "probability": round(float(probability), 4),
    }


# ---------------------------------------------------------------------------
# Prediction pipeline
# ---------------------------------------------------------------------------

class PredictionPipeline:
    """
    End-to-end prediction pipeline.

    Usage (single patient):
        >>> pipe = PredictionPipeline()
        >>> result = pipe.predict(patient_dict)

    Usage (batch):
        >>> pipe = PredictionPipeline()
        >>> results_df = pipe.predict_batch(patient_df)
    """

    def __init__(self):
        self.models_dir = os.path.join(project_config.ROOT_DIR, "models")
        self.preprocessor_path = os.path.join(self.models_dir, "preprocessor.pkl")
        self.model_path = os.path.join(self.models_dir, "xgboost_model_v2.pkl")
        self.feature_names_path = os.path.join(self.models_dir, "feature_names.json")

        self._load_artifacts()

    def _load_artifacts(self):
        """Load preprocessor, model, and feature-name list."""
        if not os.path.exists(self.preprocessor_path):
            raise NoShowException(
                f"Preprocessor not found at {self.preprocessor_path}. "
                "Run the data-transformation pipeline first."
            )
        if not os.path.exists(self.model_path):
            raise NoShowException(
                f"Model not found at {self.model_path}. "
                "Run the model-trainer pipeline first."
            )
        if not os.path.exists(self.feature_names_path):
            raise NoShowException(
                f"Feature names not found at {self.feature_names_path}. "
                "Run the data-transformation pipeline first."
            )

        self.preprocessor = load_object(self.preprocessor_path)
        self.model = load_object(self.model_path)

        with open(self.feature_names_path, "r", encoding="utf-8") as f:
            self.feature_names = json.load(f)["features"]

        logger.info("Prediction pipeline artifacts loaded successfully.")

    # ------------------------------------------------------------------
    # Input preparation helpers
    # ------------------------------------------------------------------

    def _derive_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Recreate engineered features from raw inputs so the model receives
        the exact same columns it was trained on.
        """
        df = df.copy()

        # age_group from Age
        if "Age" in df.columns and "age_group" not in df.columns:
            bins = [0, 12, 19, 59, 79, 110]
            labels = ["Child", "Teen", "Adult", "Senior", "Elderly"]
            df["age_group"] = pd.cut(
                df["Age"], bins=bins, labels=labels, right=True, include_lowest=True
            )

        # wait_bucket from days_waiting
        if "days_waiting" in df.columns and "wait_bucket" not in df.columns:
            bins = [-1, 7, 14, 30, 60, np.inf]
            labels = ["0-7", "8-14", "15-30", "31-60", "60+"]
            df["wait_bucket"] = pd.cut(df["days_waiting"], bins=bins, labels=labels)

        return df

    def _prepare_input(self, patient_dict: dict) -> pd.DataFrame:
        """
        Convert a raw patient dict into a DataFrame that matches the
        model's expected feature schema.
        """
        df = pd.DataFrame([patient_dict])
        df = self._derive_features(df)
        return self._align_features(df)

    def _align_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        One-hot encode any categoricals in ``df`` and reindex to the
        exact feature-name list the model was trained on, filling
        missing columns with 0.
        """
        # Infer categorical columns by dtype (object/category)
        cat_cols = df.select_dtypes(include=["category", "object"]).columns.tolist()
        if cat_cols:
            df = pd.get_dummies(df, columns=cat_cols, drop_first=False)

        # Reindex to training features
        df = df.reindex(columns=self.feature_names, fill_value=0)
        return df

    def _scale(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply the saved StandardScaler to declared numeric columns.
        The scaler was fit on train data in Phase 2 — we only ``transform``.
        """
        numeric_features = project_config.config.get("numeric_features", [])
        numeric_features = [c for c in numeric_features if c in df.columns]

        if numeric_features and hasattr(self.preprocessor, "transform"):
            df_scaled = df.copy()
            df_scaled[numeric_features] = self.preprocessor.transform(df[numeric_features])
            return df_scaled
        return df

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def predict(self, patient_dict: dict) -> dict:
        """
        Predict no-show probability and risk tier for a single patient.

        Parameters
        ----------
        patient_dict : dict
            Raw patient features (e.g., age, gender, days_waiting, …).

        Returns
        -------
        dict
            {"probability": float, "tier": str, "action": str}
        """
        try:
            df = self._prepare_input(patient_dict)
            df = self._scale(df)
            prob = self.model.predict_proba(df)[:, 1][0]
            result = _map_risk(prob)
            logger.info(f"Single prediction: {result}")
            return result
        except Exception as e:
            logger.error(f"Single prediction failed: {e}")
            raise NoShowException("Prediction failed", sys.exc_info()) from e

    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict no-show probability and risk tier for a batch of patients.

        Parameters
        ----------
        df : pd.DataFrame
            Raw patient features for multiple rows.

        Returns
        -------
        pd.DataFrame
            Original ``df`` with added columns:
            ``probability``, ``risk_tier``, ``recommended_action``.
        """
        try:
            df = df.copy()
            df = self._derive_features(df)
            aligned = self._align_features(df)
            aligned = self._scale(aligned)
            probs = self.model.predict_proba(aligned)[:, 1]

            df["probability"] = probs.round(4)
            risk_info = [_map_risk(p) for p in probs]
            df["risk_tier"] = [r["tier"] for r in risk_info]
            df["recommended_action"] = [r["action"] for r in risk_info]

            logger.info(f"Batch prediction completed for {len(df)} rows.")
            return df
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}")
            raise NoShowException("Batch prediction failed", sys.exc_info()) from e
