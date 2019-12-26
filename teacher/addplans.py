import sqlite3


def get_database_cursor():
    conn = sqlite3.connect("classes.db")
    conn.isolation_level = None
    return conn.cursor()


def addplans(teachername, classname, date, title, text):
    cursor = get_database_cursor()
    sql = "SELECT * from Teachingplan where Time = '%s'" % (date)
    cursor.execute(sql)
    if cursor.fetchone() is not None:
        updateplans(teachername, classname, date, title, text)
    else:
        sql2 = "INSERT into Teachingplan (TeacherName,Classname,Time,Title,Content) VALUES ('%s','%s','%s','%s','%s')" % (
            teachername, classname, date, title, text)
        cursor.execute(sql2)


def updateplans(teachername, classname, date, title, text):
    cursor = get_database_cursor()
    sql = "UPDATE Teachingplan set Content = '%s', Title = '%s' where Time = '%s' and TeacherName = '%s' and Classname = '%s'" % (
        text, title, date, teachername, classname)
    cursor.execute(sql)
