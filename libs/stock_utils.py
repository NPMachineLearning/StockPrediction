import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

def get_stock_data(stock_symbol:str, period="max"):
    """
    Get stock data from Yahoo finance by using 
    [library](https://pypi.org/project/yfinance/)

    Throw RunntimeError if stock not found
    
    Args:
      - `stock_symbol`: `str` see Yahoo finance to find symbol
        example: Tesla, Inc. (TSLA) the stock symbol is TSLA
      - `period`: `str` length of data to get refer to library.
        example: '1d'(1 day), '1mo'(1month)  

    """
    stock = yf.Ticker(stock_symbol)
    stock_data = stock.history(period=period)
    if len(stock_data) == 0:
        raise RuntimeError(f"{stock_symbol} stock not found")

    return stock_data

def convert_to_date(datetime):
  return pd.to_datetime(datetime).date

def download_stock(stock_symbol):
  try:
    # get original stock data
    stock_data = get_stock_data(stock_symbol)
    # convert original index(Date) to new column
    stock_data.insert(0, "Date", convert_to_date(stock_data.index))
    # reset index
    stock_data = stock_data.reset_index(drop=True)

    return stock_data
  except:
     raise RuntimeError(f"Unable to download {stock_symbol} data")

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