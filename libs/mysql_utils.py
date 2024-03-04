import mysql.connector as dbconnector
from sqlalchemy import create_engine
import pandas as pd
import datetime
from .db_env_utils import get_msql_db_env

def init_db() -> dbconnector.MySQLConnection:

    config = get_msql_db_env()

    connected_db = dbconnector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )
    return connected_db


def table_exists(cursor, table_name) -> bool:
    cmd = f"select table_name from information_schema.tables where table_name = '{table_name}'"
    cursor.execute(cmd)
    results = cursor.fetchall()
    if len(results) > 0:
        return True

    return False

def create_table(cursor, table_name, columns) -> bool:
    exists = table_exists(cursor, table_name)
    if not exists:
        cmd = f"create table {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, "
        for col_name, col_type in columns.items():
            cmd += f"{col_name} {col_type},"
        cmd = cmd[:-1] + ")"
        cursor.execute(cmd)
        return True

    return False

def remove_table(cursor, table_name) -> bool:
    exists = table_exists(cursor, table_name)
    if exists:
        cmd = f"drop table {table_name}"
        cursor.execute(cmd)
        return True
    
    return False

def init_SQLAlchemy_connection():
    config = get_msql_db_env()
    host=config["host"]
    user=config["user"]
    password=config["password"]
    database=config["database"]

    url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    engine = create_engine(url)
    return engine

def create_table_from_dataframe(dataframe, table_name) -> bool:
    connection = init_SQLAlchemy_connection()
    return dataframe.to_sql(name=table_name, 
                            con=connection, 
                            if_exists='replace')

def read_dataframe_from_table(table_name) -> pd.DataFrame:
    connection = init_SQLAlchemy_connection()
    cmd = f"SELECT * FROM `{table_name}`"
    df = pd.read_sql(sql=cmd, con=connection)
    return df


def test_table_CURD():
    db = init_db()
    cursor = db.cursor()
    print(table_exists(cursor, "abc211"))
    print(create_table(cursor, "abc211", {"price":"FLOAT", "pred":"FLOAT"}))
    print(table_exists(cursor, "abc211"))
    print(remove_table(cursor, "abc211"))
    print(table_exists(cursor, "abc211"))
    cursor.close()
    db.close()

def test_pandas_CURD():
    import numpy as np
    date_now = datetime.datetime.now()
    df = pd.DataFrame({"date":[date_now, 
                               (date_now+datetime.timedelta(days=3)),
                               (date_now+datetime.timedelta(days=6)),
                               (date_now+datetime.timedelta(days=6))],
                        "name": ["John", "Marry", "sus", "bt"],
                        "age": [44, 64, 77, np.nan],
                        "balance": [112.332, 2333.11, 1233.23412341234, np.nan]})

    create_table_from_dataframe(df, table_name="list")
    print(read_dataframe_from_table("list"))

if __name__ == "__main__":
    # test_table_CURD()
    test_pandas_CURD()
    
    


