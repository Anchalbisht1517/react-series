"""Training pipeline that orchestrates all data + model components end-to-end.

Usage:
    python -m src.noshow.pipeline.training_pipeline
"""

import os
import sys

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config

from noshow.components.data_ingestion import DataIngestion
from noshow.components.data_validation import DataValidation
from noshow.components.data_cleaning import DataCleaning
from noshow.components.feature_engineering import FeatureEngineering
from noshow.components.data_transformation import DataTransformation
from noshow.components.model_trainer import ModelTrainer
from noshow.components.model_evaluation import ModelEvaluation
from noshow.components.explainability import Explainability
from noshow.visualization.eda_charts import generate_all_eda_plots

logger = get_logger(__name__)


class TrainingPipeline:
    """End-to-end training orchestrator."""

    def __init__(self):
        self.ingestion = DataIngestion()
        self.validation = DataValidation()
        self.cleaning = DataCleaning()
        self.fe = FeatureEngineering()
        self.transformation = DataTransformation()
        self.trainer = ModelTrainer()
        self.evaluator = ModelEvaluation()
        self.explainer = Explainability()

    def run(self):
        try:
            logger.info("=" * 60)
            logger.info("STARTING FULL TRAINING PIPELINE")
            logger.info("=" * 60)

            # Phase 1: Data Ingestion
            logger.info("[1/8] Data Ingestion")
            raw_df = self.ingestion.initiate_data_ingestion()

            # Phase 2: Data Validation
            logger.info("[2/8] Data Validation")
            self.validation.initiate_data_validation(raw_df)

            # Phase 3: Data Cleaning
            logger.info("[3/8] Data Cleaning")
            cleaned_df = self.cleaning.initiate_data_cleaning(raw_df)

            # Phase 4: Feature Engineering
            logger.info("[4/8] Feature Engineering")
            final_df = self.fe.initiate_feature_engineering(cleaned_df)

            # Phase 5: Data Transformation
            logger.info("[5/8] Data Transformation")
            self.transformation.initiate_data_transformation(final_df)

            # Phase 6: Model Training
            logger.info("[6/8] Model Training")
            self.trainer.initiate_model_training()

            # Phase 7: Model Evaluation
            logger.info("[7/8] Model Evaluation")
            self.evaluator.initiate_model_evaluation()

            # Phase 8: SHAP Explainability
            logger.info("[8/8] SHAP Explainability")
            self.explainer.initiate_explainability()

            # Bonus: EDA Charts
            logger.info("[BONUS] EDA Charts")
            generate_all_eda_plots()

            logger.info("=" * 60)
            logger.info("TRAINING PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"Training pipeline failed: {e}")
            raise NoShowException("Training pipeline failed", sys.exc_info()) from e


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run()
