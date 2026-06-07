"""Data transformation component: train/test split, scaling, SMOTE,
and artifact persistence."""

import os
import sys
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config
from noshow.utils import save_object, write_json

logger = get_logger(__name__)


class DataTransformation:
    """
    Steps:
      1. Train / test split (stratified).
      2. One-hot encode categoricals so SMOTE can operate.
      3. StandardScaler on numeric features (fit on train).
      4. SMOTE on training split only.
      5. Save preprocessor + splits + feature names.
    """

    def __init__(self):
        self.artifacts_dir = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("artifacts_root", "artifacts"),
            "data_transformation"
        )
        self.models_dir = os.path.join(project_config.ROOT_DIR, "models")
        os.makedirs(self.artifacts_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)

        self.params = project_config.params
        self.config = project_config.config

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def split_data(self, df: pd.DataFrame):
        target_col = self.config.get("target_column", "NoShow")
        X = df.drop(columns=[target_col])
        y = df[target_col]

        split_cfg = self.params.get("split", {})
        test_size = split_cfg.get("test_size", 0.2)
        random_state = split_cfg.get("random_state", 42)
        stratify = y if split_cfg.get("stratify", True) else None

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=stratify
        )
        logger.info(
            f"Split complete | Train: {X_train.shape} | Test: {X_test.shape}"
        )
        return X_train, X_test, y_train, y_test

    def _get_numeric_features(self, X: pd.DataFrame):
        declared = self.config.get("numeric_features", [])
        return [c for c in declared if c in X.columns]

    def encode_categoricals(self, X_train: pd.DataFrame, X_test: pd.DataFrame):
        """One-hot encode all object / category columns."""
        cat_cols = X_train.select_dtypes(include=["category", "object"]).columns.tolist()
        if not cat_cols:
            logger.info("No categorical columns to encode.")
            return X_train, X_test

        logger.info(f"One-hot encoding categoricals: {cat_cols}")
        X_train = pd.get_dummies(X_train, columns=cat_cols, drop_first=False)
        X_test = pd.get_dummies(X_test, columns=cat_cols, drop_first=False)

        # Align test columns to train (fill missing with 0)
        X_test = X_test.reindex(columns=X_train.columns, fill_value=0)
        return X_train, X_test

    def scale_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame):
        numeric_features = self._get_numeric_features(X_train)
        scaler = StandardScaler()

        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()

        if numeric_features:
            X_train_scaled[numeric_features] = scaler.fit_transform(
                X_train[numeric_features]
            )
            X_test_scaled[numeric_features] = scaler.transform(
                X_test[numeric_features]
            )
            logger.info(f"Scaled numeric features: {numeric_features}")
        else:
            logger.warning("No numeric features declared for scaling.")

        # Save preprocessor artifact
        preprocessor_path = os.path.join(self.models_dir, "preprocessor.pkl")
        save_object(preprocessor_path, scaler)
        return X_train_scaled, X_test_scaled, scaler

    def apply_smote(self, X_train: pd.DataFrame, y_train: pd.Series):
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X_train, y_train)
        logger.info(f"SMOTE complete | Resampled train: {X_res.shape}")
        return X_res, y_res

    def save_artifacts(
        self,
        X_train,
        X_test,
        y_train,
        y_test,
        X_res,
        y_res,
        feature_names,
    ):
        save_object(os.path.join(self.artifacts_dir, "X_train.pkl"), X_train)
        save_object(os.path.join(self.artifacts_dir, "X_test.pkl"), X_test)
        save_object(os.path.join(self.artifacts_dir, "y_train.pkl"), y_train)
        save_object(os.path.join(self.artifacts_dir, "y_test.pkl"), y_test)
        save_object(os.path.join(self.artifacts_dir, "X_train_resampled.pkl"), X_res)
        save_object(os.path.join(self.artifacts_dir, "y_train_resampled.pkl"), y_res)

        # Feature names for inference alignment
        feature_names_path = os.path.join(self.models_dir, "feature_names.json")
        write_json(feature_names_path, {"features": list(feature_names)})
        logger.info(f"Feature names saved to {feature_names_path}")

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def initiate_data_transformation(self, df: pd.DataFrame):
        try:
            # 1. Split
            X_train, X_test, y_train, y_test = self.split_data(df)

            # 2. Encode categoricals
            X_train_enc, X_test_enc = self.encode_categoricals(X_train, X_test)

            # 3. Scale
            X_train_s, X_test_s, scaler = self.scale_features(X_train_enc, X_test_enc)

            # 4. SMOTE
            X_res, y_res = self.apply_smote(X_train_s, y_train)

            # 5. Persist
            self.save_artifacts(
                X_train_s, X_test_s, y_train, y_test,
                X_res, y_res,
                feature_names=X_train_s.columns.tolist(),
            )
            logger.info("Data transformation pipeline completed.")
            return X_train_s, X_test_s, y_train, y_test, X_res, y_res
        except Exception as e:
            logger.error(f"Data transformation failed: {e}")
            raise NoShowException("Data transformation failed", sys.exc_info()) from e


if __name__ == "__main__":
    import pandas as pd
    from noshow.components.data_ingestion import DataIngestion
    from noshow.components.data_cleaning import DataCleaning
    from noshow.components.feature_engineering import FeatureEngineering

    ingestion = DataIngestion()
    df = ingestion.load_data()
    cleaner = DataCleaning()
    cleaned_df = cleaner.initiate_data_cleaning(df)
    fe = FeatureEngineering()
    final_df = fe.initiate_feature_engineering(cleaned_df)
    transformer = DataTransformation()
    transformer.initiate_data_transformation(final_df)
    print("Data transformation complete.")
