import os
import sys
# Add this script to system path in order to access modules from different directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from libs.mysql_utils import read_dataframe_from_table, init_db, table_exists
from libs.mongo_utils import get_stock_setting, update_stock_setting
from libs.stock_utils import get_stock_data
from pydantic import BaseModel

class SettingWindow(BaseModel):
    window:int
class AddStockSymbols(BaseModel):
    symblos:list
class RemoveSymbols(AddStockSymbols):
    pass

app = FastAPI()

def dataframe_to_json(dataframe:pd.DataFrame):
    return dataframe.to_json(orient="records", date_format="iso", date_unit="s")

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

@app.get("/get-stock/{stock_symbol}")
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

@app.get("/get-stock-prediction/{stock_symbol}")
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

@app.get("/get-stock-config")
async def get_stock_config():
    try:
        config = get_stock_setting()
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
        for stock in data.symblos:
            try:
                get_stock_data(stock, "1d")
            except RuntimeError as err:
                raise HTTPException(status_code=404, detail=f"Stock {stock} not found")
            
        # https://www.mongodb.com/docs/manual/reference/operator/update/each/#definition
        values = {"stock_symbols": {"$each": data.symblos}}
        # https://www.mongodb.com/docs/manual/reference/operator/update/addToSet/
        updated_count = update_stock_setting("$addToSet", values)
        config = get_stock_setting()
        return {
            "updated_count": updated_count,
            "result":config
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})

@app.post("/remove_stocks")
async def remove_stock_symbols(data:RemoveSymbols):
    try:
        values = {"stock_symbols":  data.symblos}
        # https://www.mongodb.com/docs/manual/reference/operator/update/pullAll/
        updated_count = update_stock_setting("$pullAll", values)
        config = get_stock_setting()
        return {
            "updated_count": updated_count,
            "result":config
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": err})