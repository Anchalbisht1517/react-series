"""Data validation component: asserts schema, dtypes, and null rules."""

import os
import sys
import pandas as pd

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config
from noshow.utils import read_yaml, write_yaml

logger = get_logger(__name__)


class DataValidation:
    """
    Validates incoming raw data against the schema defined in
    ``config/schema.yaml``.
    """

    def __init__(self):
        schema_path = os.path.join(project_config.CONFIG_DIR, "schema.yaml")
        self.schema = read_yaml(schema_path) if os.path.exists(schema_path) else {}

        self.validation_dir = os.path.join(
            project_config.ROOT_DIR,
            project_config.config.get("artifacts_root", "artifacts"),
            "data_validation"
        )
        os.makedirs(self.validation_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Validation checks
    # ------------------------------------------------------------------

    def validate_columns(self, df: pd.DataFrame) -> bool:
        expected = set(self.schema.get("columns", []))
        actual = set(df.columns)
        missing = expected - actual
        if missing:
            raise NoShowException(f"Missing expected columns: {missing}")
        extra = actual - expected
        if extra:
            logger.warning(f"Unexpected extra columns detected: {extra}")
        logger.info("Column validation passed.")
        return True

    def validate_dtypes(self, df: pd.DataFrame) -> bool:
        expected_dtypes = self.schema.get("dtypes", {})
        for col, expected_dtype in expected_dtypes.items():
            if col not in df.columns:
                continue
            actual_dtype = str(df[col].dtype)

            if expected_dtype == "datetime64[ns]":
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    raise NoShowException(
                        f"Column '{col}' expected datetime but got {actual_dtype}"
                    )
            elif actual_dtype != expected_dtype:
                # Allow flexible int/float overlap (e.g., int64 vs Int64)
                logger.warning(
                    f"Column '{col}' dtype {actual_dtype} != expected {expected_dtype}"
                )
        logger.info("Dtype validation passed.")
        return True

    def validate_nulls(self, df: pd.DataFrame) -> bool:
        total = len(df)
        tolerances = self.schema.get("null_tolerance", {})
        default_tol = tolerances.get("default", 0.0)

        for col in df.columns:
            allowed = tolerances.get(col, default_tol)
            null_pct = df[col].isnull().mean()
            if null_pct > allowed:
                raise NoShowException(
                    f"Column '{col}' has {null_pct:.2%} nulls (limit {allowed})"
                )
        logger.info("Null validation passed.")
        return True

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def initiate_data_validation(self, df: pd.DataFrame) -> bool:
        try:
            self.validate_columns(df)
            self.validate_dtypes(df)
            self.validate_nulls(df)

            report = {
                "status": "passed",
                "rows": int(len(df)),
                "columns": list(df.columns),
            }
            write_yaml(os.path.join(self.validation_dir, "validation_report.yaml"), report)
            logger.info("Data validation completed successfully.")
            return True
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            raise NoShowException("Data validation failed", sys.exc_info()) from e


if __name__ == "__main__":
    import pandas as pd
    from noshow.components.data_ingestion import DataIngestion

    ingestion = DataIngestion()
    df = ingestion.load_data()
    validator = DataValidation()
    validator.initiate_data_validation(df)
    print("Validation complete.")
