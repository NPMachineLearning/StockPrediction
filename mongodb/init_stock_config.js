db = connect("mongodb://localhost/stocks");
db.config.insertOne({ window: 7 });
db.stocks.insertOne({ stock_symbols: ["GC=F"] });
