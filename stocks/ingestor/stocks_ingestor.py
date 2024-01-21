from utils.stock_utils import get_stock_data
from utils.utils import setup_logging
from utils.mysql_utils import init_db, create_table_from_dataframe
import logging
import pandas as pd

def convert_to_date(datetime):
  return pd.to_datetime(datetime).date

def ingest_stocks(stock_symbols:list):
  list_successful = []
  list_fail = []

  db = init_db()

  for stock in stock_symbols:
    try:
      logging.info(f"Downloading {stock} stock data .....")
      stock_data = get_stock_data(stock)
      stock_data.index = convert_to_date(stock_data.index)
      stock_data = stock_data.rename_axis("Date", axis=0)
      logging.info(f"Downloading {stock} stock data completed")

      logging.info(f"Writting {stock} data into database .....")
      create_table_from_dataframe(stock_data, stock)
      logging.info(f"Writting {stock} data into database completed")
      list_successful.append(stock)
    except Exception as err:
      logging.error(err)
      list_fail.append(stock)

  db.close()
  
  return {"successful": list_successful,
          "fail": list_fail} 