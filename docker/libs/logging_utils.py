import logging
from logging import Logger
import sys
import os

def setup_logging(out_filename:str, level=logging.INFO):
    """
    Setup general logging
    """
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler(out_filename),
                            logging.StreamHandler()
                        ],
                        level=level)

def get_logger(out_filename:str, level=logging.INFO):
    """
    Get logging instance
    """
    logger = logging.getLogger(out_filename)
    logger.setLevel(level=level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(level=level)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(out_filename)
    file_handler.setLevel(level=level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    return logger

def clean_log(file_path:str, size_threshold:int=500000000):
    """
    Clean log file by replace content with empty string
    Args:
         - `file_path`: `str` path to log file
         - `size_threshold`: `int` in byte log file will be 
            cleaned only if log file size is greater than this byte value
            default is 500000000 byte(500mb)  
    """
    if os.stat(file_path).st_size > size_threshold:
            open(file_path, "w").close()

def close_logger(logger:Logger):
     if logger is not None:
        for handler in logger.handlers:
            logger.removeHandler(handler)
            handler.close()

