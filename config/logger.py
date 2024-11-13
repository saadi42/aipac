import logging
import os

def setup_logger():
    """Sets up the root logger with the specified configuration."""
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Avoid adding multiple handlers if setup_logger is called more than once
    if not logger.handlers:
        logger.addHandler(handler)
