"""Central logging utility for the no-show predictor project."""

import logging
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Logger configuration
# ---------------------------------------------------------------------------
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Formatter shared across handlers
FORMATTER = logging.Formatter(
    fmt="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ---------------------------------------------------------------------------
# Helper to fetch a configured logger instance
# ---------------------------------------------------------------------------

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Return a logger with both file and stream handlers.

    Parameters
    ----------
    name : str
        Logger name, typically ``__name__``.
    level : int, optional
        Logging level (default: ``logging.INFO``).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(LOG_FILE, mode="a")
        file_handler.setFormatter(FORMATTER)
        logger.addHandler(file_handler)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(FORMATTER)
        logger.addHandler(stream_handler)

    return logger
