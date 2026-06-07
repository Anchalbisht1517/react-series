"""Unit tests for the prediction pipeline."""

import os
import sys
import unittest
import pandas as pd
import numpy as np

# Ensure src is on the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from noshow.pipeline.prediction_pipeline import PredictionPipeline, _map_risk


class TestRiskMapping(unittest.TestCase):
    """Test threshold logic in isolation (no model required)."""

    def test_high_risk(self):
        result = _map_risk(0.80)
        self.assertEqual(result["tier"], "High")
        self.assertEqual(result["action"], "Call + SMS reminder")
        self.assertAlmostEqual(result["probability"], 0.80)

    def test_medium_risk(self):
        result = _map_risk(0.50)
        self.assertEqual(result["tier"], "Medium")
        self.assertEqual(result["action"], "SMS reminder")

    def test_low_risk(self):
        result = _map_risk(0.25)
        self.assertEqual(result["tier"], "Low")
        self.assertEqual(result["action"], "Standard appointment")

    def test_boundary_high_medium(self):
        result = _map_risk(0.65)
        self.assertEqual(result["tier"], "Medium")

    def test_boundary_medium_low(self):
        result = _map_risk(0.40)
        self.assertEqual(result["tier"], "Medium")


class TestPredictionPipeline(unittest.TestCase):
    """
    Integration tests that require artifacts from Phases 2–4.
    If artifacts are missing, tests are skipped with an informative message.
    """

    @classmethod
    def setUpClass(cls):
        cls.artifacts_exist = True
        models_dir = os.path.join(project_root, "models")
        required = ["preprocessor.pkl", "xgboost_model_v2.pkl", "feature_names.json"]
        for f in required:
            if not os.path.exists(os.path.join(models_dir, f)):
                cls.artifacts_exist = False
                break

    def setUp(self):
        if not self.artifacts_exist:
            self.skipTest("Model artifacts not found. Run training pipeline first.")
        self.pipeline = PredictionPipeline()

    def test_single_prediction_structure(self):
        """Predict on a synthetic patient dict; assert output keys."""
        patient = {
            "Age": 30,
            "Gender": 0,
            "Scholarship": 0,
            "Hypertension": 0,
            "Diabetes": 0,
            "Alcoholism": 0,
            "Handicap": 0,
            "SMS_received": 1,
            "days_waiting": 5,
            "appointment_weekday": 2,
            "previous_no_shows": 0,
            "Neighbourhood": "JARDIM DA PENHA",
        }
        result = self.pipeline.predict(patient)
        self.assertIn("probability", result)
        self.assertIn("tier", result)
        self.assertIn("action", result)
        self.assertIsInstance(result["probability"], float)
        self.assertTrue(0.0 <= result["probability"] <= 1.0)

    def test_batch_prediction_shape(self):
        """Predict on a tiny DataFrame; assert added columns."""
        df = pd.DataFrame([
            {"Age": 25, "Gender": 0, "Scholarship": 0, "Hypertension": 0,
             "Diabetes": 0, "Alcoholism": 0, "Handicap": 0, "SMS_received": 1,
             "days_waiting": 3, "appointment_weekday": 1, "previous_no_shows": 0,
             "Neighbourhood": "JARDIM DA PENHA"},
            {"Age": 60, "Gender": 1, "Scholarship": 1, "Hypertension": 1,
             "Diabetes": 0, "Alcoholism": 0, "Handicap": 0, "SMS_received": 0,
             "days_waiting": 45, "appointment_weekday": 4, "previous_no_shows": 2,
             "Neighbourhood": "JARDIM DA PENHA"},
        ])
        result_df = self.pipeline.predict_batch(df)
        self.assertIn("probability", result_df.columns)
        self.assertIn("risk_tier", result_df.columns)
        self.assertIn("recommended_action", result_df.columns)
        self.assertEqual(len(result_df), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
