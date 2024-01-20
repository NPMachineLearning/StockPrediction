import logging

def setup_logging(out_filename:str):
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        handlers=[
                            logging.FileHandler(out_filename),
                            logging.StreamHandler()
                        ],
                        level=logging.INFO)
