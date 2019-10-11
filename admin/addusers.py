import sqlite3


def get_database_cursor():
    conn = sqlite3.connect("users.db")
    conn.isolation_level = None
    return conn.cursor()


def addusers(username, identity, password=123456):
    cursor = get_database_cursor()
    sql = "INSERT into User (Name,Password,Type) VALUES ('%s','%s',%s)" % (username, password, identity)
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
