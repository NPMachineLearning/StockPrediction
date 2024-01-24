db = connect("mongodb://localhost/stocks");
db.config.insertOne({ window: 1 });
db.stocks.insertOne({ stock_symbols: ["BTC-USD", "GC=F"] });
