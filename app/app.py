import streamlit as st
import api
import plotly.graph_objects as go
import pandas as pd

# get all stocks information
stocks = api.get_stocks()

# st.write(stocks)

option = st.selectbox("Select a stock", 
             [s["name"] for s in stocks])

selected_stock = list(filter(lambda x: True if x["name"]==option else False, stocks))[0]
selected_stock_name = selected_stock["name"]
selected_stock_symbol = selected_stock["symbol"]
st.write(f"selected stock name: {selected_stock_name}")
st.write(f"selected stock symbol: {selected_stock_symbol}")

# get selected stock data
stock_data = api.get_stock_data(selected_stock_symbol)

# convert stock data to dataframe
df = pd.DataFrame(stock_data)
# st.write(df)

# create figure with plotly
fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'])
                     ])

# show stock data
st.plotly_chart(fig, use_container_width=False, theme=None)