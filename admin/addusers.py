import sqlite3


def get_database_cursor():
    conn = sqlite3.connect("users.db")
    conn.isolation_level = None
    return conn.cursor()


def addusers(username, password, identity, realname):
    cursor = get_database_cursor()
    sql = "INSERT into User (Name,Password,Type,Realname) VALUES ('%s','%s',%s,'%s')" % (
        username, password, identity, realname)
    cursor.execute(sql)


def findusers(username):
    cursor = get_database_cursor()
    sql = "SELECT * FROM User where Name = '%s'" % username
    cursor.execute(sql)
    if cursor.fetchone() is not None:
        return True
    else:
        return False


def findusertype(usertype):
    if usertype == "教师/Teacher":
        return 0
    if usertype == "学生/Student":
        return 1
    if usertype == "游客/Visitor":
        return 2
    if usertype == "管理员/Admin":
        return 3


def selectusers():
    cursor = get_database_cursor()
    sql = "SELECT Name FROM User"
    cursor.execute(sql)
    return cursor.fetchall()


def resetusers(username):
    cursor = get_database_cursor()
    sql = "Update User Set Password='123456' where Name = '%s'" % username
    cursor.execute(sql)


def deleteusers(username):
    cursor = get_database_cursor()
    sql = "Delete from User where Name = '%s'" % username
    cursor.execute(sql)
