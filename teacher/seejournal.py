import sqlite3
import time


def get_database_cursor():
    conn = sqlite3.connect("users.db")
    conn.isolation_level = None
    return conn.cursor()


def create_pinboard(text):
    cursor = get_database_cursor()
    localtime = time.asctime(time.localtime(time.time()))
    sql = "INSERT into Pinboard (Text,Time) VALUES ('%s','%s')" % (text, localtime)
    cursor.execute(sql)


def reply_pinboard(text, reply):
    # TODO:Since there is no ID, need to transport the text first to identify which one to reply
    cursor = get_database_cursor()
    sql = "UPDATE Pinboard set Reply = '%s' where Text = '%s'" % (reply, text)
    cursor.execute(sql)


def delete_pinboard(text):
    cursor = get_database_cursor()
    sql = "Delete from Pinboard where Text = '%s'" % (text)
    cursor.execute(sql)


def get_all_messages():
    cursor = get_database_cursor()
    sql = "select * FROM Journal";
    cursor.execute(sql)
    return cursor.fetchall()


def dropusers(name):
    cursor = get_database_cursor()
    sql = "delete from User where Name = '%s'" % (name)
    cursor.execute(sql)
    return cursor.fetchall()
