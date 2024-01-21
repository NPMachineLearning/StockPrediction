import yfinance as yf
from utils.mysql_utils import read_dataframe_from_table, create_table_from_dataframe
from sklearn.ensemble import RandomForestRegressor
import logging
import pandas as pd
import time

def get_stock_data(stock_symbol:str, period="max"):
    stock = yf.Ticker(stock_symbol)
    stock_data = stock.history(period=period)
    if len(stock_data) == 0:
        raise RuntimeError(f"{stock_symbol} stock not found")

    return stock_data

def convert_to_date(datetime):
  return pd.to_datetime(datetime).date

def ingest_stocks(stock_symbols:list):
  list_successful = []
  list_fail = []

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
  
  return {"successful": list_successful,
          "fail": list_fail} 

def prepare_data_for_training(stock_df, window=7, target_colum_name="Close"):
   # get stock Close values
    data = stock_df[[target_colum_name]]

    # rename to Price
    data = data.rename(columns={"Close": "Price"})

    # mean of a period(window) for training 
    data["Period"] = data["Price"].rolling(window).mean()
    data = data.dropna()

    # Shift Price back 1 row since we are predicting
    # 1 future day by a period(window)
    data = data.assign(Price=data["Price"].shift(-1))
    data = data.dropna()

    # prepare X, y training and target data
    X = data[["Period"]].to_numpy()
    y = data["Price"]

    return X, y

def train_model(X, y):
    # train model
    model = RandomForestRegressor()
    model.fit(X, y)
    
    return model