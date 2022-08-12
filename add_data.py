import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error

def DBConnect(dbName=None):
    conn = mysql.connect(host='localhost', user='root', password='tigraymearey14',
                         database=dbName, buffered=True)
    cur = conn.cursor()
    return conn, cur

def emojiDB(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
    cur.execute(dbQuery)
    conn.commit()

def createDB(dbName: str) -> None:
    conn, cur = DBConnect()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};") # creating database
    conn.commit()
    cur.close()

def createTables(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    sqlFile = 'schema_data.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')

    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    cur.close()

    return

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    cols_2_drop = ['original_text']
    try:
        df = df.drop(columns=cols_2_drop, axis=1)
        df = df.fillna(0)
    except KeyError as e:
        print("Error:", e)

    return df


def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    conn, cur = DBConnect(dbName)

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO TweetDataTable (created_at, source, subjectivity, polarity, language,
                    favorite_count, retweet_count, followers_count, friends_count,
                    hashtags, user_mentions, place, clean_text)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                row[12])

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            conn.commit()
            #print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return

def db_execute_fetch(*args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:

    connection, cursor1 = DBConnect(**kwargs)
    if many:
        cursor1.executemany(*args)
    else:
        cursor1.execute(*args)

    # get column names
    field_names = [i[0] for i in cursor1.description]

    # get column values
    res = cursor1.fetchall()

    # get row count and show info
    nrow = cursor1.rowcount
    if tablename:
        print(f"{nrow} recrods fetched from {tablename} table")

    cursor1.close()
    connection.close()

    # return result
    if rdf:
        return pd.DataFrame(res, columns=field_names)
    else:
        return res
if __name__ == "__main__":
    print("sucessfully")
    dbName='tweet_db'
    createDB(dbName)
    emojiDB(dbName='tweet_db')
    createTables(dbName)
    df = pd.read_csv('cleaned_data/cleaned_data_final.csv')
    insert_to_tweet_table(dbName='tweet_db', df=df, table_name='TweetInformation')
    print("sucessfully")