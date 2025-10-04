# logging_config.py
import logging

def get_logger(name: str = None):
    """
    Returns a logger. If name is not given, it uses the caller module's name.
    """
    logger = logging.getLogger(name if name else __name__)
    logger.setLevel(logging.DEBUG)

    # Handlers
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh = logging.FileHandler("app.log")
    fh.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
