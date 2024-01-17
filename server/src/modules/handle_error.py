import logging

# def setup_logger():
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.INFO)
#     handler = logging.FileHandler(f"{__name__}.log", mode='w')
#     formatter = logging.Formatter("%(asctime)s %(message)s")
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     return logger

# logger = setup_logger()

def handle_error(error):
    # logger.info(f'Error in {__name__} file. The error is: "{error}"')
    return error
