# -*- coding: utf-8 -*-
"""Yahoo_Stock_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CbA4lXxgG5gIPTFgLEDqNuPylD6Co_HY
"""
import os
import sys
# Add docker directory to path
sys.path.insert(1, os.path.join(os.getcwd(), "docker"))

from libs.logging_utils import get_logger, close_logger, clean_log
import pandas as pd
import numpy as np
from libs.stock_utils import train_model, prepare_data_for_training, download_stock, get_stock_info
from libs.mysql_utils import create_table_from_dataframe
from libs.mongo_utils import get_stock_setting, update_stock_currency
import time
import datetime

LOG_DIR = "./logs"
INFO_LOG_FILE_PATH = "./logs/stock_processor.log"
ERROR_LOG_FILE_PATH = "./logs/stock_processor_error.log"

def make_stock_forcast(model, x, window=7):
  if isinstance(x, np.ndarray):
    # flatten
    x = x.reshape(-1)
    x = pd.Series(x)
  elif not isinstance(x, pd.Series):
    raise RuntimeError(f"x must either be a pandas Series or numpy array")
  
  data_rolled = x.rolling(window).mean()
  data_rolled = data_rolled.dropna()
  data_rolled = data_rolled.to_numpy()
  forecasts = model.predict(np.expand_dims(data_rolled, axis=1))
  return forecasts


def run():
  try:
    if not os.path.exists(LOG_DIR):
      os.mkdir(LOG_DIR)

    info_logger = get_logger(INFO_LOG_FILE_PATH)
    error_logger = get_logger(ERROR_LOG_FILE_PATH)
    clean_log(INFO_LOG_FILE_PATH)
    clean_log(INFO_LOG_FILE_PATH)

    # get configuration
    stock_config = get_stock_setting()
    
    # stock that will be processed
    stocks = stock_config["stocks"]

    # period of data for training model
    window = stock_config["window"]

    # iterate over stocks and do processing
    for stock in stocks:
      stock_symbol = stock['symbol']

      info_logger.info(f"----------- Processing {stock_symbol} stock -----------")

      info_logger.info(f"Downloading data .....")
      stock_df = download_stock(stock_symbol)
      info_logger.info(f"Downloading data completed")

      ## skip for writing original stock data into database
      # logging.info(f"Writting data into database .....")
      # create_table_from_dataframe(stock_data_df, stock_symbol)
      # logging.info(f"Writting data into database completed")

      ## update stock information
      info_logger.info("Writting stock info ....")
      stock_info = get_stock_info(stock_symbol)
      currency = stock_info["currency"]
      update_stock_currency(stock_symbol, currency)
      info_logger.info("Writting stock info completed")
      
      ## Prepare data for training model
      info_logger.info(f"Prepare stock data for model training")
      ## skip for reading dataframe from database
      # stock_df = read_dataframe_from_table(stock_symbol)
      X, y = prepare_data_for_training(stock_df=stock_df,
                                      window=window,
                                      target_colum_name="Close")
      info_logger.info(f"Prepare stock data for model training completed")

      ## Training the model ##
      info_logger.info(f"Training model ......")
      t1 = time.time()
      model = train_model(X=X, y=y)
      t2 = time.time()
      info_logger.info(f"Training model completed")
      info_logger.info(f"Training time -> {t2-t1} seconds")

      ## Make forecasting ##
      info_logger.info(f"Forcasting .....")
      forecasts = make_stock_forcast(model=model, 
                                    x=stock_df["Close"], 
                                    window=window)
      info_logger.info(f"Forcasting completed")

      # Create DataFrame for forecast
      info_logger.info(f"Creating DataFrame from forecast .....")
      
      # make a new row to be append to stock dataframe
      # because we forecast next day
      new_row = pd.DataFrame([[np.nan]*len(stock_df.columns)], 
                            columns=stock_df.columns,)
      
      # create the date object of next day forecast 
      new_date = stock_df["Date"].values[-1]+datetime.timedelta(days=1)

      # add new row to stock dataframe
      stock_df = pd.concat([stock_df, new_row]).reset_index(drop=True)
      
      # set forecast
      dates = stock_df["Date"].copy()
      dates.iloc[-1] = new_date
      stock_df["Date"] = dates
      
      # create forecast dataframe
      forecast_df = pd.DataFrame(data={"Prediction": forecasts,
                                      "Date": stock_df["Date"][window:]})
      info_logger.info(f"Creating DataFrame from forecast completed")

      ## Merge stock DataFrame with forecast DataFrame ##
      info_logger.info(f"Merging stock and forcast data .....")
      stock_df = stock_df.merge(forecast_df, on="Date", how="outer")

      # reset index
      stock_df = stock_df.reset_index(drop=True)
      info_logger.info(f"Merging stock and forcast data completed")

      ## Writing final stock data back to database ##
      info_logger.info(f"Writing stock and forecast data into database .....")
      create_table_from_dataframe(stock_df, stock_symbol)
      info_logger.info(f"Writing stock and forecast data into database completed")

      info_logger.info(f"----------- Processing {stock_symbol} stock completed -----------")

    close_logger(info_logger)
    close_logger(error_logger)
  except Exception as err:
    error_logger.error(err)
    close_logger(info_logger)
    close_logger(error_logger)
    print(err, flush=True)

if __name__ == "__main__":
  run()