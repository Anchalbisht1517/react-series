"""Main entry point for the no-show predictor training pipeline.

Usage:
    python main.py
"""

from noshow.logger import get_logger
from noshow.pipeline.training_pipeline import TrainingPipeline

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("No-show predictor training pipeline started.")
    pipeline = TrainingPipeline()
    pipeline.run()
