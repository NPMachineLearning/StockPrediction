import os
import sys
# Add root directory to path
sys.path.insert(1, os.getcwd())
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import json
from libs.mysql_utils import read_dataframe_from_table, init_db, table_exists
from libs.mongo_utils import get_stock_setting, update_stock_setting, get_stock_currency
from libs.stock_utils import get_stock_data
from pydantic import BaseModel, Field

class SettingWindow(BaseModel):
    window:int
class AddStockSymbols(BaseModel):
    stocks:list = Field(examples=['[{"name":"Gold", "symbol":"GC=F"}]'])
class RemoveSymbols(AddStockSymbols):
    pass

app = FastAPI()

def dataframe_to_json(dataframe:pd.DataFrame, py_object=True):
    """
    Convert pandas dataframe to json

    Args:
        - `dataframe`: pandas dataframe
        - `py_object`: True(default) will convert dataframe to python dictionary
            otherise False as string of Json
    """
    json_str = dataframe.to_json(orient="records", date_format="iso", date_unit="s")
    if json_str:
        if py_object:
            return json.loads(json_str)
        else:
            return json_str
    else:
        raise RuntimeError("Unable to convert dataframe to json string")

def is_stock_exists(stock_symbol:str):
    # check if stock table exists in database
    exist = False
    with init_db() as db:
        with db.cursor() as cursor:
            exist = table_exists(cursor, stock_symbol)
    return exist

def check_stock_exists(stock_symbol:str):
    """
    If a stock not exist raise HTTPException
    """
    if not is_stock_exists(stock_symbol):
        raise HTTPException(status_code=404, 
            detail=f"stock {stock_symbol} not found")


@app.get("/")
async def root():
    return {"message": "Hello stock service with fastapi"}

@app.get("/get_stock_currency/{stock_symbol}")
async def get_stock(stock_symbol:str):
    try:
        currency = get_stock_currency(stock_symbol)
        if currency:
            return {"result":currency}
        else:
            raise Exception(f"No currency for symbol {stock_symbol}")
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})

@app.get("/get_stock/{stock_symbol}")
async def get_stock(stock_symbol:str):
    try:
        check_stock_exists(stock_symbol)
        
        stock_df = read_dataframe_from_table(stock_symbol)
        
        # remove last column which is prediction
        # remove first column which is index
        col_names = stock_df.columns[1:-1]
        stock_df = stock_df[col_names]
        # remove any row with no data
        stock_df = stock_df.dropna()
        return {
            "stock": stock_symbol,
            "size": len(stock_df),
            "result": dataframe_to_json(stock_df)
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})

@app.get("/get_stock_prediction/{stock_symbol}")
async def get_stock_prediction(stock_symbol:str):
    try:
        check_stock_exists(stock_symbol)

        stock_df = read_dataframe_from_table(stock_symbol)

        stock_df = stock_df[["Date", "Prediction"]]
        stock_df = stock_df.dropna()
        return {
            "stock": stock_symbol,
            "size": len(stock_df),
            "result": dataframe_to_json(stock_df)
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})

@app.get("/get_stock_config")
async def get_stock_config():
    try:
        filter_stocks = []
        config = get_stock_setting()
        for stock in config["stocks"]:
            if is_stock_exists(stock["symbol"]):
                filter_stocks.append(stock)
        config["stocks"] = filter_stocks
        return {
            "result":config
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})

@app.post("/update_window")
async def update_stock_window(data:SettingWindow):
    try:
        # https://www.mongodb.com/docs/manual/reference/operator/update/set/#-set
        updated_count = update_stock_setting("$set", {"window": data.window})
        config = get_stock_setting()
        return {
            "updated_count": updated_count,
            "result":config
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})

@app.post("/add_stocks")
async def add_stock_symbols(data:AddStockSymbols):
    try:
        # pre check whether if a stock exists or not in Yahoo finance
        for stock in data.stocks:
            symbol = stock["symbol"]
            try:
                get_stock_data(symbol, "1d")
            except RuntimeError as err:
                raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
            
        # https://www.mongodb.com/docs/manual/reference/operator/update/each/#definition
        values = {"stocks": {"$each": data.stocks}}
        # https://www.mongodb.com/docs/manual/reference/operator/update/addToSet/
        update_stock_setting("$addToSet", values)
        config = get_stock_setting()
        return {
            "result":config
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})

@app.post("/remove_stocks")
async def remove_stock_symbols(data:RemoveSymbols):
    try:
        values = {"stocks":  data.stocks}
        # https://www.mongodb.com/docs/manual/reference/operator/update/pullAll/
        update_stock_setting("$pullAll", values)
        config = get_stock_setting()
        return {
            "result":config
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})