import logging

def setup_logger(log_file_path='/var/log/errors.log'):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(log_file_path, mode='a')
    
    formatter = logging.Formatter("%(asctime)s %(message)s")
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

logger = setup_logger(log_file_path='/var/log/errors.log')

def handle_error(error):
    logger.info(f'The error is: "{error}"')
    return str(error)