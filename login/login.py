import sqlite3


def get_database_cursor():
    conn = sqlite3.connect("users.db")
    conn.isolation_level = None
    return conn.cursor()


def get_correct_password(username):
    cursor = get_database_cursor()
    sql = "SELECT Password from User where name = '%s'" % username
    cursor.execute(sql)
    return cursor.fetchone()


def get_user_type(username):
    cursor = get_database_cursor()
    sql = "SELECT Type from User where name = '%s'" % username
    cursor.execute(sql)
    return cursor.fetchone()


def redirect_page_type(type: str):
    if int(type) == 0:
        return "teacherindex"
    if int(type) == 1:
        return "studentindex"
    if int(type) == 3:
        return "adminindex"
    raise Exception("Wrong UserType!")
