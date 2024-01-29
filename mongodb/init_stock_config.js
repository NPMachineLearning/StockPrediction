db = connect("mongodb://localhost/stock_config");
// config here is collection name
db.config.insertOne({
  window: 7,
  stocks: [{ name: "Gold Feb 24", symbol: "GC=F" }],
});
