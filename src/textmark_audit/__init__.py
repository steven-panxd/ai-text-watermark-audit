"""Tools for auditing machine-readable signals in text."""

from .compare import compare_text
from .scanner import scan_text

__all__ = ["compare_text", "scan_text"]
__version__ = "0.1.0"
