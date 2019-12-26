import sqlite3


def get_database_cursor():
    conn = sqlite3.connect("users.db")
    conn.isolation_level = None
    return conn.cursor()


# return whether there is a protection for this user
def find_student_protection(username):
    cursor = get_database_cursor()
    sql = "SELECT * FROM Studentprotection where Username = '%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        return True


def add_student_protection(type, answer, username):
    cursor = get_database_cursor()
    if find_student_protection(username) is True:
        print("Already exist")
    else:
        sql = "INSERT into Studentprotection (Type,Answer,Username) VALUES('%s','%s','%s')" % (type, answer, username)
        cursor.execute(sql)


def verify_student_protection(type, answer, username):
    cursor = get_database_cursor()
    if find_student_protection(username) is False:
        print("There is no protection for you")
    else:
        sql = "SELECT * FROM Studentprotection where Type = %s and Answer = '%s' and Username = '%s'" % (type, answer, \
                                                                                                         username)
        cursor.execute(sql)
        if cursor.fetchone() is None:
            print("Wrong answer")
        else:
            print("Right!")
