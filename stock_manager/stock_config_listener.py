import os
import sys
# Add root directory to path
sys.path.insert(1, os.getcwd())

from stock_processor import run
from libs.logging_utils import get_logger, clean_log, close_logger
from libs.mongo_utils import get_database

LOG_DIR = "./logs"
INFO_LOG_FILE_PATH = "./logs/stock_config_listener.log"
ERROR_LOG_FILE_PATH = "./logs/stock_config_listener_error.log"

def main():
    global resumeToken
    resumeToken = None

    try:
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
        info_logger = get_logger(INFO_LOG_FILE_PATH)
        error_logger = get_logger(ERROR_LOG_FILE_PATH)
        clean_log(INFO_LOG_FILE_PATH)
        clean_log(ERROR_LOG_FILE_PATH)
        
        
        db = get_database()
        collection = db.get_collection("config")
        pipeline  = [{
                '$match': {
                    'operationType': { '$in': ['update', 'replace'] },
                }
            }]
        
        if resumeToken:
            change_stream  = collection.watch(pipeline=pipeline, resume_after=resumeToken)
        else:

            change_stream  = collection.watch(pipeline=pipeline)

        # start change stream
        for change in change_stream:
            print(change)
            info_logger.info(f"----------- Detect stock config file updated -----------")
            info_logger.info(change)
            info_logger.info(f"----------- Run stock processor -----------")
            run()

        close_logger(info_logger)
        close_logger(error_logger)
    except Exception as err:
        resumeToken = change_stream.resume_token
        error_logger.error(err)
        close_logger(info_logger)
        close_logger(error_logger)
        print(err, flush=True)
        main()

if __name__ == "__main__":
    main()