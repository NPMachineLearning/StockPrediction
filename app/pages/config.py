import streamlit as st
import api
import time

st.title("Stock Management")

if st.button("Home", 
             help="Back to home to see stock data and prediction",
             type="primary"):
    st.switch_page("app.py")

st.markdown("""
To find 📈 stock symbol go to **[Yahoo Finance](https://finance.yahoo.com/)** and find
stock's symbol

For example: Bitcoin USD (BTC-USD) where ***Bitcoin USD*** is **name** and ***BTC-USD*** is **symbol**
""")

mg_option = st.selectbox("What do you want to do?", ["Add a new stock",
                                                     "Remove a stock"])

if mg_option == "Add a new stock":
    st.subheader("Add a stock")
    add_col1, add_col2 = st.columns(2)

    with add_col1:
        add_stock_name = st.text_input("Stock name:", placeholder="Name")

    with add_col2:
        add_stock_symbol = st.text_input("Stock symbol:", placeholder="Symbol")

    if st.button("Add"):
        with st.spinner(f"Adding {add_stock_name} ....."):
            time.sleep(1.0)
            if add_stock_name and add_stock_symbol:
                try:
                    res = api.add_stock(add_stock_name, add_stock_symbol)
                    st.success(f"Add stock {add_stock_name}({add_stock_symbol}) successful!!")
                    # time.sleep(2.0)
                    # st.rerun()
                except Exception as err:
                    st.error(f"{err}, find stock symbol here https://finance.yahoo.com/", icon="😞")
            else:
                if add_stock_name == "":
                    st.error("Missing stock name")
                elif add_stock_symbol == "":
                    st.error("Missing stock symbol")

if mg_option == "Remove a stock":
    st.subheader("Remove a stock")
    # get all stocks information
    stocks = api.get_stocks()
    rm_stock_option = st.selectbox("Select a stock", 
                                    [s["name"] for s in stocks],
                                    index=None,
                                    placeholder="Select a stock to remove")

    if st.button("Remove"):
        with st.spinner(f"Removing {rm_stock_option} ......"):
            time.sleep(1.0)
            if rm_stock_option:
                try:
                    rm_stock = list(filter(lambda x: True if x["name"]==rm_stock_option else False, stocks))[0]
                    rm_stock_name = rm_stock["name"]
                    rm_stock_symbol = rm_stock["symbol"]
                    res = api.remove_stock(rm_stock_name, rm_stock_symbol)
                    st.success(f"Remove stock {rm_stock_name}({rm_stock_symbol}) successful!!")
                    time.sleep(2.0)
                    st.rerun()
                except Exception as err:
                    st.error(err)
            else:
                st.error("Select a stock from list to remove", icon="😞")