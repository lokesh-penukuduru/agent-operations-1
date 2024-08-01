import logging
import os

from pythonjsonlogger import jsonlogger


def get_logger(name):
    log_handler = logging.StreamHandler()
    log_formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(message)s %(name)s %(host)s",
        rename_fields={"asctime": "time", "levelname": "level"},
    )
    log_handler.setFormatter(log_formatter)

    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    try:
        logger.setLevel(os.environ["LOG_LEVEL"])
    except (KeyError, ValueError):
        logger.warning(
            "Incorrect LOG_LEVEL env variable. Setting the logger level to INFO."
        )
        logger.setLevel(logging.INFO)

    return logger