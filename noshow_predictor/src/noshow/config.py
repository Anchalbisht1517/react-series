"""Configuration loader for the no-show predictor project."""

import os
from typing import Any, Dict

from noshow.utils import read_yaml
from noshow.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

class ProjectConfig:
    """
    Lightweight wrapper around the project's YAML configuration files.
    Loads ``config.yaml``, ``params.yaml``, and ``schema.yaml`` lazily.
    """

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    CONFIG_DIR = os.path.join(ROOT_DIR, "config")
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    ARTIFACTS_DIR = os.path.join(ROOT_DIR, "artifacts")
    MODELS_DIR = os.path.join(ROOT_DIR, "models")
    OUTPUTS_DIR = os.path.join(ROOT_DIR, "outputs")

    def __init__(self):
        self._config: Dict[str, Any] = None
        self._params: Dict[str, Any] = None
        self._schema: Dict[str, Any] = None

    # -- Lazy loaders -------------------------------------------------------

    @property
    def config(self) -> Dict[str, Any]:
        if self._config is None:
            path = os.path.join(self.CONFIG_DIR, "config.yaml")
            self._config = read_yaml(path) if os.path.exists(path) else {}
            logger.info(f"Loaded config from {path}")
        return self._config

    @property
    def params(self) -> Dict[str, Any]:
        if self._params is None:
            path = os.path.join(self.CONFIG_DIR, "params.yaml")
            self._params = read_yaml(path) if os.path.exists(path) else {}
            logger.info(f"Loaded params from {path}")
        return self._params

    @property
    def schema(self) -> Dict[str, Any]:
        if self._schema is None:
            path = os.path.join(self.CONFIG_DIR, "schema.yaml")
            self._schema = read_yaml(path) if os.path.exists(path) else {}
            logger.info(f"Loaded schema from {path}")
        return self._schema

    # -- Convenience accessors --------------------------------------------

    def get(self, key: str, default: Any = None, section: str = "config") -> Any:
        """
        Retrieve a nested key from a config section using dot notation.

        Parameters
        ----------
        key : str
            Dot-separated key, e.g. ``model.scale_pos_weight``.
        default : Any, optional
            Fallback value if the key is missing.
        section : str
            One of ``config``, ``params``, or ``schema``.

        Returns
        -------
        Any
            The requested value or ``default``.
        """
        source = getattr(self, section, {})
        keys = key.split(".")
        val = source
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val


# Singleton instance
project_config = ProjectConfig()
