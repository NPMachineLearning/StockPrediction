import streamlit as st
import api
import plotly.graph_objects as go
import pandas as pd

st.title("Stock Prediction")

# get all stocks information
stocks = api.get_stocks()

def get_financial_data_graph(graph_type, df, stock_name="stock"):
    if graph_type == "Candlestick":
        return go.Candlestick(x=df["Date"],
                              open=df['Open'], high=df['High'],
                              low=df['Low'], close=df['Close'], 
                              showlegend=True, name=stock_name)
    elif graph_type == "Line":
        return go.Scatter(x=df["Date"], y=df["Close"],
                         showlegend=True, name=stock_name)
    elif graph_type == "OHLC":
        return go.Ohlc(x=df["Date"],
                         open=df['Open'], high=df['High'],
                         low=df['Low'], close=df['Close'], 
                         showlegend=True, name=stock_name)
    elif graph_type == "Bar":
        return go.Bar(x=df["Date"], y=df["Close"],
                         showlegend=True, name=stock_name)
    return None

# st.write(stocks)

stock_option = st.selectbox("Select a stock", 
             [s["name"] for s in stocks])

selected_stock = list(filter(lambda x: True if x["name"]==stock_option else False, stocks))[0]
selected_stock_name = selected_stock["name"]
selected_stock_symbol = selected_stock["symbol"]
# st.write(f"selected stock name: {selected_stock_name}")
# st.write(f"selected stock symbol: {selected_stock_symbol}")

graph_option = st.selectbox("Select a graph",
                            ["Candlestick",
                             "Line",
                             "OHLC",
                             "Bar"])

# get selected stock data
stock_data = api.get_stock_data(selected_stock_symbol)

# convert stock data to dataframe
stock_df = pd.DataFrame(stock_data)
# st.write(df)

stock_prediction = api.get_stock_prediction(selected_stock_symbol)
pred_df = pd.DataFrame(stock_prediction)
# st.write(pred_df)

# create figure with plotly
# fig = go.Figure(data=[go.Candlestick(x=df['Date'],
#                 open=df['Open'], high=df['High'],
#                 low=df['Low'], close=df['Close'])
#                      ])
fig = go.Figure(data=[get_financial_data_graph(graph_type=graph_option, df=stock_df, stock_name=stock_option),
                     go.Line(x=pred_df["Date"], y=pred_df["Prediction"], 
                             showlegend=True, name="Prediction")],
                     layout=go.Layout(autosize=True, 
                                      hovermode="x", 
                                      xaxis={"title":"Date",
                                             "rangeslider":dict(
                                                  visible=True
                                             ),
                                             "type":"date",
                                             "rangeselector":dict(
                                                  buttons=list([
                                                      dict(count=7,
                                                            label="1w",
                                                            step="day",
                                                            stepmode="backward"),
                                                       dict(count=1,
                                                            label="1m",
                                                            step="month",
                                                            stepmode="backward"),
                                                       dict(count=6,
                                                            label="6m",
                                                            step="month",
                                                            stepmode="backward"),
                                                       dict(count=1,
                                                            label="YTD",
                                                            step="year",
                                                            stepmode="todate"),
                                                       dict(count=1,
                                                            label="1y",
                                                            step="year",
                                                            stepmode="backward"),
                                                       dict(step="all")
                                                  ])
                                             )},
                                      yaxis={"title":"Price($USD)"},
                                      title=f"{stock_option} data and prediction"))

# show stock data
st.plotly_chart(fig, use_container_width=False, theme=None)