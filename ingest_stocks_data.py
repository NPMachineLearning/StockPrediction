from stock_utils import get_stock_data
from utils import setup_logging
from mysql_utils import init_db, create_table_from_dataframe
import logging

setup_logging("ingest_stocks.log")

STOCK_SYMBOL = "GC=F"
db = init_db()

try:
  logging.info(f"Downloading stock data for {STOCK_SYMBOL} .....")
  stock_data = get_stock_data(STOCK_SYMBOL)
  logging.info(f"Downloading stock data for {STOCK_SYMBOL} finished")

  logging.info(f"Writting {STOCK_SYMBOL} into database .....")
  create_table_from_dataframe(stock_data, STOCK_SYMBOL)
  logging.info(f"Writting {STOCK_SYMBOL} into database finished")
except Exception as err:
  logging.error(err)

db.close()