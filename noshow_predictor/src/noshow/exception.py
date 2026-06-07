"""Custom exception class for the no-show predictor project."""

import sys
import traceback
from typing import Optional


class NoShowException(Exception):
    """
    Generic project exception that captures the originating file name,
    line number, and a human-readable error message.
    """

    def __init__(self, message: str, error_detail: Optional[sys.exc_info] = None):
        """
        Parameters
        ----------
        message : str
            High-level description of what went wrong.
        error_detail : tuple, optional
            Result of ``sys.exc_info()`` for deeper traceback context.
        """
        super().__init__(message)
        self.message = message
        self.error_detail = error_detail

        if error_detail:
            exc_type, exc_value, exc_tb = error_detail
            self.file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "unknown"
            self.line_number = exc_tb.tb_lineno if exc_tb else 0
        else:
            self.file_name = "unknown"
            self.line_number = 0

    def __str__(self) -> str:
        return (
            f"[{self.__class__.__name__}] {self.message} | "
            f"File: {self.file_name} | Line: {self.line_number}"
        )

    def to_log_string(self) -> str:
        """Return full traceback string suitable for logging."""
        if self.error_detail:
            return "".join(traceback.format_exception(*self.error_detail))
        return str(self)
