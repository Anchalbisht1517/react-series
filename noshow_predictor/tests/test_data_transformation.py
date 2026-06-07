"""Unit tests for data transformation component."""

import os
import sys
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from noshow.components.data_transformation import DataTransformation
from noshow.components.feature_engineering import FeatureEngineering
from noshow.components.data_cleaning import DataCleaning
from noshow.components.data_ingestion import DataIngestion
from noshow.utils import load_object


class TestDataTransformation(unittest.TestCase):
    """Test train/test split, scaling, and artifact persistence."""

    @classmethod
    def setUpClass(cls):
        # Build pipeline up to transformation if artifacts missing
        artifacts_dir = os.path.join(project_root, "artifacts", "data_transformation")
        cls.X_train_path = os.path.join(artifacts_dir, "X_train.pkl")
        if not os.path.exists(cls.X_train_path):
            # Run upstream pipeline
            ingestion = DataIngestion()
            df = ingestion.load_data()
            cleaning = DataCleaning()
            cleaned = cleaning.clean(df)
            fe = FeatureEngineering()
            final = fe.engineer_features(cleaned)
            transformer = DataTransformation()
            transformer.initiate_data_transformation(final)

    def test_train_test_split_exists(self):
        """X_train, X_test, y_train, y_test artifacts should exist."""
        for name in ["X_train.pkl", "X_test.pkl", "y_train.pkl", "y_test.pkl"]:
            path = os.path.join(project_root, "artifacts", "data_transformation", name)
            self.assertTrue(os.path.exists(path), f"Missing {name}")

    def test_smote_applied(self):
        """Resampled train set should be larger than original train."""
        X_train = load_object(self.X_train_path)
        X_res = load_object(os.path.join(project_root, "artifacts", "data_transformation", "X_train_resampled.pkl"))
        self.assertGreater(len(X_res), len(X_train))

    def test_preprocessor_saved(self):
        """preprocessor.pkl should exist in models/."""
        path = os.path.join(project_root, "models", "preprocessor.pkl")
        self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
