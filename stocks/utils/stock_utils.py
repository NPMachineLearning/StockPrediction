import yfinance as yf

def get_stock_data(stock_symbol:str, period="max"):
    stock = yf.Ticker(stock_symbol)
    stock_data = stock.history(period=period)
    if len(stock_data) == 0:
        raise RuntimeError(f"{stock_symbol} stock not found")

    return stock_data