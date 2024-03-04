/** This javascript will run by MongoDB at first time */

// get database stock_config
db = connect("mongodb://localhost/stock_config");

// config here is collection name
// then insert some data from Yahoo finance
// https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF
// https://finance.yahoo.com/quote/SI=F?p=SI=F&.tsrc=fin-srch
db.config.insertOne({
  window: 7,
  stocks: [
    { name: "Gold 24", symbol: "GC=F" },
    { name: "Silver 24", symbol: "SI=F" },
  ],
});
