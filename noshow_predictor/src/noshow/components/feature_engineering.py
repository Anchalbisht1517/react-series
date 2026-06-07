"""Feature engineering component: creates derived features and produces the
final modeling dataset."""

import os
import sys
import numpy as np
import pandas as pd

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config

logger = get_logger(__name__)


class FeatureEngineering:
    """
    Engineered features:
      - days_waiting
      - age_group (binned)
      - appointment_weekday (0=Mon)
      - wait_bucket (binned)
      - previous_no_shows (cumulative per patient)
    """

    def __init__(self):
        self.processed_path = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("data", {}).get("processed_path", "data/processed/cleaned_appointments_v3.csv")
        )
        os.makedirs(os.path.dirname(self.processed_path), exist_ok=True)

    # ------------------------------------------------------------------
    # Feature creators
    # ------------------------------------------------------------------

    def create_days_waiting(self, df: pd.DataFrame) -> pd.DataFrame:
        """Waiting time in whole days; drops negative values."""
        df = df.copy()
        # Ensure datetime dtype (defensive for CSV round-trips)
        df["ScheduledDay"] = pd.to_datetime(df["ScheduledDay"], errors="coerce")
        df["AppointmentDay"] = pd.to_datetime(df["AppointmentDay"], errors="coerce")
        df["days_waiting"] = (
            df["AppointmentDay"].dt.floor("D") - df["ScheduledDay"].dt.floor("D")
        ).dt.days

        before = len(df)
        df = df[df["days_waiting"] >= 0]
        after = len(df)
        if before != after:
            logger.info(f"Removed {before - after:,} rows with negative days_waiting.")
        return df

    def create_age_group(self, df: pd.DataFrame) -> pd.DataFrame:
        bins = [0, 12, 19, 59, 79, 110]
        labels = ["Child", "Teen", "Adult", "Senior", "Elderly"]
        df["age_group"] = pd.cut(
            df["Age"], bins=bins, labels=labels, right=True, include_lowest=True
        )
        return df

    def create_appointment_weekday(self, df: pd.DataFrame) -> pd.DataFrame:
        df["appointment_weekday"] = df["AppointmentDay"].dt.dayofweek  # Monday = 0
        return df

    def create_wait_bucket(self, df: pd.DataFrame) -> pd.DataFrame:
        bins = [-1, 7, 14, 30, 60, np.inf]
        labels = ["0-7", "8-14", "15-30", "31-60", "60+"]
        df["wait_bucket"] = pd.cut(df["days_waiting"], bins=bins, labels=labels)
        return df

    def create_previous_no_shows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cumulative no-shows *before* each appointment per patient.
        Requires PatientId and sorted dates.
        """
        df = df.sort_values(["PatientId", "AppointmentDay"])
        df["previous_no_shows"] = (
            df.groupby("PatientId")["NoShow"]
            .transform(lambda x: x.shift(1).cumsum())
            .fillna(0)
            .astype(int)
        )
        return df

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.create_days_waiting(df)
        df = self.create_age_group(df)
        df = self.create_appointment_weekday(df)
        df = self.create_wait_bucket(df)
        df = self.create_previous_no_shows(df)

        # Drop columns not needed for modeling
        drop_cols = ["PatientId", "AppointmentID", "ScheduledDay", "AppointmentDay"]
        drop_cols = [c for c in drop_cols if c in df.columns]
        df = df.drop(columns=drop_cols)

        logger.info(f"Feature engineering complete. Final shape: {df.shape}")
        return df

    def initiate_feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            final_df = self.engineer_features(df)
            final_df.to_csv(self.processed_path, index=False)
            logger.info(f"Processed dataset saved to {self.processed_path}")
            return final_df
        except Exception as e:
            logger.error(f"Feature engineering failed: {e}")
            raise NoShowException("Feature engineering failed", sys.exc_info()) from e


if __name__ == "__main__":
    import pandas as pd
    from noshow.components.data_ingestion import DataIngestion
    from noshow.components.data_cleaning import DataCleaning

    ingestion = DataIngestion()
    df = ingestion.load_data()
    cleaner = DataCleaning()
    cleaned_df = cleaner.initiate_data_cleaning(df)
    fe = FeatureEngineering()
    final_df = fe.initiate_feature_engineering(cleaned_df)
    print(f"Feature engineering complete: {final_df.shape}")
