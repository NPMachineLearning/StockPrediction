db = connect("mongodb://localhost/stock_config");
// config here is collection name
db.config.insertOne({ window: 7, stock_symbols: ["GC=F"] });
