import logging
import os


def setup_logger(log_file_path="/var/log/errors.log"):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file_path, mode="a")
    formatter = logging.Formatter("%(asctime)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def handle_error(error):
    logger = setup_logger(os.environ.get("ERROR_HANDLER", "/var/log/errors.log"))
    logger.info(f"The error is: {error}")
    return str(error)
