from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from utils.mysql_utils import read_dataframe_from_table, init_db, table_exists

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