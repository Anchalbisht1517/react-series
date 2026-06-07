"""Common utility functions used across the no-show predictor project."""

import os
import yaml
import json
import joblib
from typing import Any, Dict

from noshow.logger import get_logger
from noshow.exception import NoShowException

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------

def read_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load a YAML file and return its contents as a dictionary.

    Parameters
    ----------
    file_path : str
        Absolute or relative path to the YAML file.

    Returns
    -------
    dict
        Parsed YAML content.

    Raises
    ------
    NoShowException
        If the file is missing or cannot be parsed.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
        logger.info(f"YAML loaded successfully from {file_path}")
        return content or {}
    except Exception as e:
        logger.error(f"Failed to load YAML from {file_path}: {e}")
        raise NoShowException(f"YAML read error: {file_path}") from e


def write_yaml(file_path: str, data: Dict[str, Any]) -> None:
    """
    Serialize a dictionary to a YAML file.

    Parameters
    ----------
    file_path : str
        Target path for the YAML file.
    data : dict
        Data to serialize.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False)
        logger.info(f"YAML written successfully to {file_path}")
    except Exception as e:
        logger.error(f"Failed to write YAML to {file_path}: {e}")
        raise NoShowException(f"YAML write error: {file_path}") from e


def read_json(file_path: str) -> Dict[str, Any]:
    """
    Load a JSON file and return its contents as a dictionary.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Returns
    -------
    dict
        Parsed JSON content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        logger.info(f"JSON loaded successfully from {file_path}")
        return content
    except Exception as e:
        logger.error(f"Failed to load JSON from {file_path}: {e}")
        raise NoShowException(f"JSON read error: {file_path}") from e


def write_json(file_path: str, data: Dict[str, Any]) -> None:
    """
    Serialize a dictionary to a JSON file with indentation.

    Parameters
    ----------
    file_path : str
        Target path for the JSON file.
    data : dict
        Data to serialize.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info(f"JSON written successfully to {file_path}")
    except Exception as e:
        logger.error(f"Failed to write JSON to {file_path}: {e}")
        raise NoShowException(f"JSON write error: {file_path}") from e


# ---------------------------------------------------------------------------
# Model artifact helpers
# ---------------------------------------------------------------------------

def save_object(file_path: str, obj: Any) -> None:
    """
    Persist an arbitrary Python object using ``joblib``.

    Parameters
    ----------
    file_path : str
        Destination path (typically ``.pkl``).
    obj : Any
        Object to serialize.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        joblib.dump(obj, file_path)
        logger.info(f"Object saved to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save object to {file_path}: {e}")
        raise NoShowException(f"Save object error: {file_path}") from e


def load_object(file_path: str) -> Any:
    """
    Load a previously saved Python object using ``joblib``.

    Parameters
    ----------
    file_path : str
        Path to the serialized object.

    Returns
    -------
    Any
        Deserialized object.
    """
    try:
        obj = joblib.load(file_path)
        logger.info(f"Object loaded from {file_path}")
        return obj
    except Exception as e:
        logger.error(f"Failed to load object from {file_path}: {e}")
        raise NoShowException(f"Load object error: {file_path}") from e


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def ensure_dir(path: str) -> str:
    """
    Ensure a directory exists; create it if necessary.

    Parameters
    ----------
    path : str
        Directory path.

    Returns
    -------
    str
        The ensured directory path.
    """
    os.makedirs(path, exist_ok=True)
    return path
