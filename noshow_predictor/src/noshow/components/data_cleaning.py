"""Data cleaning component: fixes anomalies, renames, encodes, and prepares
raw data for feature engineering."""

import os
import sys
import pandas as pd

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config

logger = get_logger(__name__)


class DataCleaning:
    """
    Cleaning steps:
      1. Coerce date columns to datetime.
      2. Remove invalid ages (< 0 or > 110).
      3. Rename columns (Hipertension, Handcap, No-show).
      4. Encode target (NoShow) and Gender.
      5. Return cleaned DataFrame (IDs and dates retained for FE).
    """

    def __init__(self):
        self.cleaning_dir = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("artifacts_root", "artifacts"),
            "data_cleaning"
        )
        os.makedirs(self.cleaning_dir, exist_ok=True)

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # 1. Datetime coercion (defensive)
        df["ScheduledDay"] = pd.to_datetime(df["ScheduledDay"], errors="coerce")
        df["AppointmentDay"] = pd.to_datetime(df["AppointmentDay"], errors="coerce")
        invalid_dates = df["ScheduledDay"].isnull().sum() + df["AppointmentDay"].isnull().sum()
        if invalid_dates:
            logger.warning(f"Found {invalid_dates} unparseable date entries.")

        # 2. Age bounds
        before = len(df)
        df = df[(df["Age"] >= 0) & (df["Age"] <= 110)]
        after = len(df)
        if before != after:
            logger.info(f"Removed {before - after:,} rows with invalid Age.")

        # 3. Rename
        rename_map = {
            "Hipertension": "Hypertension",
            "Handcap": "Handicap",
            "No-show": "NoShow",
        }
        df = df.rename(columns=rename_map)

        # 4. Encode target
        if not pd.api.types.is_numeric_dtype(df["NoShow"]):
            df["NoShow"] = df["NoShow"].map({"Yes": 1, "No": 0})
            logger.info("Encoded NoShow: Yes->1, No->0")

        # 5. Encode Gender
        if not pd.api.types.is_numeric_dtype(df["Gender"]):
            df["Gender"] = df["Gender"].map({"F": 0, "M": 1})
            logger.info("Encoded Gender: F->0, M->1")

        logger.info(f"Cleaning complete. Shape: {df.shape}")
        return df

    def initiate_data_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            cleaned_df = self.clean(df)
            artifact_path = os.path.join(self.cleaning_dir, "cleaned_data.csv")
            cleaned_df.to_csv(artifact_path, index=False)
            logger.info(f"Cleaning artifact saved to {artifact_path}")
            return cleaned_df
        except Exception as e:
            logger.error(f"Data cleaning failed: {e}")
            raise NoShowException("Data cleaning failed", sys.exc_info()) from e


if __name__ == "__main__":
    import pandas as pd
    from noshow.components.data_ingestion import DataIngestion

    ingestion = DataIngestion()
    df = ingestion.load_data()
    cleaner = DataCleaning()
    cleaned_df = cleaner.initiate_data_cleaning(df)
    print(f"Cleaning complete: {cleaned_df.shape}")
