from utils.stock_utils import get_stock_data
from utils.utils import setup_logging
from utils.mysql_utils import init_db, create_table_from_dataframe
import logging


def ingest_stocks(stock_symbols:list):
  list_successful = []
  list_fail = []

  db = init_db()

  for symbol in stock_symbols:
    try:
      logging.info(f"Downloading {symbol} stock data .....")
      stock_data = get_stock_data(symbol)
      logging.info(f"Downloading {symbol} stock data completed")

      logging.info(f"Writting {symbol} data into database .....")
      create_table_from_dataframe(stock_data, symbol)
      logging.info(f"Writting {symbol} data into database completed")
      list_successful.append(symbol)
    except Exception as err:
      logging.error(err)
      list_fail.append(symbol)

  db.close()
  
  return {"successful": list_successful,
          "fail": list_fail} 