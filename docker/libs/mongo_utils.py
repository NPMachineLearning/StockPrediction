from pymongo import MongoClient
from .db_env_utils import get_mongo_db_env
from urllib.parse import quote_plus
import uuid

def get_database(database_name=None):
    """
    Get monog database
    
    Args:
        - `database_name`: `str` database to connect, if None then use default `stock_config`.
    """   
    env = get_mongo_db_env()

    # Create a connection using MongoClient
    CONNECTION_STRING = "mongodb://%s:%s@%s/?replicaSet=rs0" % (quote_plus(env["user"]), 
                                                quote_plus(env["password"]), 
                                                env["host"])
    client = MongoClient(CONNECTION_STRING)

    # Return database
    return client[env["database"] if database_name is None else database_name]

def get_stock_setting():
    db  = get_database()
    collection = db["config"]
    config = collection.find_one({} ,{'_id': False})
    db.client.close()
    return config

def update_stock_setting(operator:str, dict_value):
    """
    Update one document in config collection
    Args:
     - `operator`: `str` see [here](https://www.mongodb.com/docs/manual/reference/operator/update/)
     - `dict_value`: `dictionary` field:value mapping where field is key in document or can be operator  
    """
    db  = get_database()
    collection = db["config"]
    result = collection.update_one({}, {
        operator:dict_value
    })
    db.client.close()

def update_stock_currency(symbol:str, currency:str):
    db  = get_database()
    collection = db["currency"]
    doc = collection.find_one({"symbol":symbol})
    if doc:
        result = collection.update_one({"symbol":symbol}, {
            "$set":{"currency":currency}
        })
    else:
        result = collection.insert_one({"symbol":symbol, "currency":currency})
    db.client.close()

def get_stock_currency(symbol:str):
    db  = get_database()
    collection = db["currency"]
    doc = collection.find_one({"symbol":symbol}, {'_id': False})
    db.client.close()
    return doc

def test_create_and_drop_collection():
    db = get_database()
    collection_name = 'a_collection_test'
    collection = db[collection_name]
    assert collection_name == collection.name, "create collection fail"
    db[collection_name].drop()
    db.client.close()

def test_insert_and_find():
    db = get_database()
    collection_name = "a_test_list"
    collection = db[collection_name]
    try:
        john = {"_id": str(uuid.uuid1()),
                "name": "John",
                "age": 32}
        ken = {"_id": str(uuid.uuid1()),
            "name": "Ken",
            "age": 12}
        results = collection.insert_many([john, ken])
        print(results.inserted_ids)
        print(f"number of data: {collection.count_documents({})}")
        item = collection.find_one({"name": john["name"]})
        assert john["name"] == item["name"], "insert data fail"
        item = collection.find_one({"name": ken["name"]})
        assert ken["age"] == item["age"], "insert data fail"
    finally:
        db[collection_name].drop()
        db.client.close()

def test_set_get_currency():
    try:
        update_stock_currency(symbol="GC=F", currency="USD")
        stock_currency = get_stock_currency("GC=F")
        assert stock_currency["symbol"]=="GC=F" and stock_currency["currency"]=="USD", "update currency CG=F fail"

        update_stock_currency(symbol="GC=J", currency="JPN")
        stock_currency = get_stock_currency("GC=J")
        assert stock_currency["symbol"]=="GC=J" and stock_currency["currency"]=="JPN", "update currency CG=F fail" 

    finally:
        db = get_database()
        db["currency"].drop()
        db.client.close()

    
if __name__ == "__main__":
    test_create_and_drop_collection()   
    test_insert_and_find()
    test_set_get_currency()
    
