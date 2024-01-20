import mysql.connector as dbconnector
from sqlalchemy import create_engine
import pandas as pd
import datetime


def init_db(host="localhost",
            user="root",
            password="mysql-password",
            database="stocks") -> dbconnector.MySQLConnection:
    global HOST
    global USER
    global PASSWORD
    global DATABASE

    HOST = host
    USER = user
    PASSWORD = password
    DATABASE = database

    connected_db = dbconnector.connect(
        host=host,
        user=user,
        password=password,
        database=database
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

def create_table_from_dataframe(dataframe, table_name) -> bool:
    print(USER)
    url = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
    engine = create_engine(url)
    return dataframe.to_sql(name=table_name, 
                            con=engine, 
                            if_exists='replace',
                            index_label="id")

def remove_table(cursor, table_name) -> bool:
    exists = table_exists(cursor, table_name)
    if exists:
        cmd = f"drop table {table_name}"
        cursor.execute(cmd)
        return True
    
    return False

# db = init_db()
# cursor = db.cursor()
# # print(table_exists(cursor, "abc211"))
# # print(create_table(cursor, "abc211", {"price":"FLOAT", "pred":"FLOAT"}))
# # print(table_exists(cursor, "abc211"))
# # print(remove_table(cursor, "abc211"))
# # print(table_exists(cursor, "abc211"))
# df = pd.DataFrame({"date":[datetime.datetime.now().date(), 
#                                                   (datetime.datetime.now()+datetime.timedelta(days=3)).date(),
#                                                   (datetime.datetime.now()+datetime.timedelta(days=6)).date()],
#                                           "name": ["John", "Marry", "sus"],
#                                           "age": [44, 64, 77],
#                                           "balance": [112.332, 2333.11, 1233.23412341234]})

# create_table_from_dataframe(df, table_name="list")
# cursor.close()
# db.close()


