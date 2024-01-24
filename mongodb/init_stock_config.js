db = connect("mongodb://localhost/stocks");
db.config.insertOne({ window: 1 });
