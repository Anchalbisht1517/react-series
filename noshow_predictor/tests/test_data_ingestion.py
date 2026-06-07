"""Unit tests for data ingestion component."""

import os
import sys
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from noshow.components.data_ingestion import DataIngestion
from noshow.exception import NoShowException


class TestDataIngestion(unittest.TestCase):
    """Test data ingestion loading and artifact creation."""

    def setUp(self):
        self.ingestion = DataIngestion()

    def test_load_data_shape(self):
        """Raw data should load with 14 columns."""
        df = self.ingestion.load_data()
        self.assertEqual(df.shape[1], 14)
        self.assertIn("No-show", df.columns)

    def test_datetime_parsing(self):
        """ScheduledDay and AppointmentDay should be datetime."""
        df = self.ingestion.load_data()
        self.assertTrue(
            str(df["ScheduledDay"].dtype).startswith("datetime")
        )
        self.assertTrue(
            str(df["AppointmentDay"].dtype).startswith("datetime")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
