from pymongo import MongoClient
from utils.db_env_utils import get_mongo_db_env
from urllib.parse import quote_plus
import uuid

def get_database(database_name=None):   
    env = get_mongo_db_env()

    # Create a connection using MongoClient
    CONNECTION_STRING = "mongodb://%s:%s@%s" % (quote_plus(env["user"]), 
                                                quote_plus(env["password"]), 
                                                env["host"])
    client = MongoClient(CONNECTION_STRING)

    # Return database
    return client[env["database"] if database_name is None else database_name]

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
    
if __name__ == "__main__":
    test_create_and_drop_collection()   
    test_insert_and_find()
    
