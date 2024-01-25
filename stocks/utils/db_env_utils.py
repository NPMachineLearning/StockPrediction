import os
from dotenv import load_dotenv

def get_msql_db_env():
    load_dotenv()
    env = {
        "host": os.environ["MYSQL_HOST"],
        "user": os.environ["MYSQL_USER"], 
        "password": os.environ["MYSQL_PASSWORD"], 
        "database": os.environ["MYSQL_DATABASE"],  
    }
    
    return env

def get_mongo_db_env():
    load_dotenv()
    env = {
        "host": os.environ["MONGO_HOST"],
        "user": os.environ["MONGO_USER"], 
        "password": os.environ["MONGO_PASSWORD"], 
        "database": os.environ["MONGO_DATABASE"],  
    }
    
    return env