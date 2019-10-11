import sqlite3


def get_database_cursor():
    # Todo: the path of db may recity after uploaded to the server
    conn = sqlite3.connect("../classes.db")
    conn.isolation_level = None
    return conn.cursor()

def addexperience(date,title,text):
    cursor=get_database_cursor()
    sql2="INSERT into Teachingexperience (Time,Title,Content) VALUES ('%s','%s','%s')"%(date,title,text)
    cursor.execute(sql2)



#things beneath it are for testing!
def showusers():
    cursor = get_database_cursor()
    sql = "select * FROM Teachingexperience"
    cursor.execute(sql)
    return cursor.fetchall()

def dropusers(name):
    cursor=get_database_cursor()
    sql ="delete from Teachingexperience where Title = '%s'"%(name)
    cursor.execute(sql)
    return cursor.fetchall()

