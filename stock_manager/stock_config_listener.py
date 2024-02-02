import os
import sys
from stock_processor import run
# Add root directory to path
sys.path.insert(1, os.getcwd())

from libs.logging_utils import setup_logging
from libs.mongo_utils import get_database
import logging

if __name__ == "__main__":
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    setup_logging("./logs/stock_processor.log")
    
    db = get_database()
    collection = db.get_collection("config")
    change_stream  = collection.watch([{
        '$match': {
            'operationType': { '$in': ['update', 'insert', 'replace', 'delete'] },
        }
    }])

    for change in change_stream:
        logging.info(f"----------- Detect stock config file updated -----------")
        logging.info(f"----------- Run stock processor -----------")
        run()