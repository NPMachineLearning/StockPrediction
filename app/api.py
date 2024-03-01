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

def get_stock_prediction(stock_symbol):
    res = requests.get(urljoin(SERVER, f"get-stock-prediction/{stock_symbol}"))
    return res.json()["result"]

def add_stock(stock_name, stock_symbol):
    res = requests.post(urljoin(SERVER, "add_stocks/"), 
                        json={"stocks":[{"name":stock_name, "symbol":stock_symbol}]})
    if res.status_code == 200:
        return res.json()["result"]
    elif res.status_code == 404:
        msg = res.json()["detail"]
        raise Exception(f"{msg}")
    else:
        raise Exception("Something went wrong!!")

def remove_stock(stock_name, stock_symbol):
    res = requests.post(urljoin(SERVER, "remove_stocks/"), 
                        json={"stocks":[{"name":stock_name, "symbol":stock_symbol}]})
    if res.status_code == 200:
        return res.json()["result"]
    else:
        raise Exception("Something went wrong!!")
    