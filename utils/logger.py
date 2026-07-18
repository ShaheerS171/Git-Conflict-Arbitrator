"""
utils/logger.py

Central logging configuration for the Git Conflict Arbitrator.

Features
--------
- Console logging
- File logging
- Automatic log directory creation
- Prevents duplicate handlers
- UTF-8 file encoding
"""

from __future__ import annotations

import logging
from pathlib import Path

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

LOG_LEVEL = logging.INFO

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"

LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = (
    "[%(asctime)s] "
    "[%(levelname)s] "
    "[%(name)s] "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ------------------------------------------------------------
# Logger Factory
# ------------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger.

    Example
    -------
    logger = get_logger(__name__)

    logger.info("Application started")
    logger.error("Something failed")
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # --------------------------------------------------------
    # Console Handler
    # --------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(LOG_LEVEL)

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # --------------------------------------------------------
    # File Handler
    # --------------------------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setLevel(LOG_LEVEL)

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


# ------------------------------------------------------------
# Default Logger
# ------------------------------------------------------------

logger = get_logger("GitConflictArbitrator")