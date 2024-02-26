import requests
from urllib.parse import urljoin

SERVER = "http://localhost:8002"

def get_config():
    res = requests.get(urljoin(SERVER, "get-stock-config"))
    return res.json()

def get_window():
    data = get_config()
    return data["result"]["window"]

def get_stocks():
    data = get_config()
    return data["result"]["stocks"]

def get_stock_data(stock_symbol):
    res = requests.get(urljoin(SERVER, f"get-stock/{stock_symbol}"))
    return res.json()["result"]