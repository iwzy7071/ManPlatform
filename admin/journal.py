import sqlite3
import time

def get_database_cursor():
    conn = sqlite3.connect("users.db")
    conn.isolation_level = None
    return conn.cursor()

def create_journal(text):
    cursor = get_database_cursor()
    localtime = time.asctime(time.localtime(time.time()))
    sql = "INSERT into Journal (Time,Text) VALUES ('%s','%s')"%(localtime,text)
    cursor.execute(sql)




