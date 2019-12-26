import sqlite3


def get_database_cursor():
    conn = sqlite3.connect("classes.db")
    conn.isolation_level = None
    return conn.cursor()


def addexperience(teachername, date, title, text):
    cursor = get_database_cursor()
    sql2 = "INSERT into Teachingexperience (Teachername,Time,Title,Content) VALUES ('%s','%s','%s','%s')" % (
    teachername, date, title, text)
    cursor.execute(sql2)


def showusers():
    cursor = get_database_cursor()
    sql = "select distinct(Teachername) FROM Teachingexperience"
    cursor.execute(sql)
    return cursor.fetchall()


def showcontents(name):
    cursor = get_database_cursor()
    sql = "select * FROM Teachingexperience where Teachername = '%s'" % (name)
    cursor.execute(sql)
    return cursor.fetchall()


