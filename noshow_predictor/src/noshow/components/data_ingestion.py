"""Data ingestion component: loads raw CSV and persists ingestion artifact."""

import os
import sys
import pandas as pd

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config

logger = get_logger(__name__)


class DataIngestion:
    """
    Responsible for loading the raw Kaggle CSV into a pandas DataFrame.
    Parses date columns immediately so downstream components receive
    proper dtypes.
    """

    def __init__(self):
        raw_path = project_config.config.get("data", {}).get("raw_path")
        self.raw_path = os.path.join(project_config.ROOT_DIR, raw_path) \
            if not os.path.isabs(raw_path) else raw_path

        self.ingestion_dir = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("artifacts_root", "artifacts"),
            "data_ingestion"
        )
        os.makedirs(self.ingestion_dir, exist_ok=True)

    def load_data(self) -> pd.DataFrame:
        """Load CSV and parse datetime columns."""
        if not os.path.exists(self.raw_path):
            raise NoShowException(
                f"Raw dataset not found at {self.raw_path}. "
                "Please manually place 'KaggleV2-May-2016.csv' inside data/raw/"
            )

        df = pd.read_csv(
            self.raw_path,
            parse_dates=["ScheduledDay", "AppointmentDay"],
            dtype={
                "Scholarship": "int64",
                "Hipertension": "int64",
                "Diabetes": "int64",
                "Alcoholism": "int64",
                "Handcap": "int64",
                "SMS_received": "int64",
            }
        )
        logger.info(f"Raw data loaded successfully: {df.shape}")
        return df

    def save_artifact(self, df: pd.DataFrame) -> None:
        """Persist a copy of the raw DataFrame for traceability."""
        artifact_path = os.path.join(self.ingestion_dir, "raw.csv")
        df.to_csv(artifact_path, index=False)
        logger.info(f"Ingestion artifact saved to {artifact_path}")

    def initiate_data_ingestion(self) -> pd.DataFrame:
        """Execute ingestion pipeline step."""
        try:
            df = self.load_data()
            self.save_artifact(df)
            return df
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise NoShowException("Data ingestion failed", sys.exc_info()) from e


if __name__ == "__main__":
    ingestion = DataIngestion()
    df = ingestion.initiate_data_ingestion()
    print(f"Ingestion complete: {df.shape}")
