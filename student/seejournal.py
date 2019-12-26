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


def get_classes_database_cursor():
    conn = sqlite3.connect("classes.db")
    conn.isolation_level = None
    return conn.cursor()


def get_users_database_cursor():
    conn = sqlite3.connect("users.db")
    conn.isolation_level = None
    return conn.cursor()


def check_in_class(course, username):
    cursor = get_classes_database_cursor()
    sql = "SELECT * from Classnamelist where Username = '%s' and Classname = '%s'" % (username, course)
    cursor.execute(sql)
    if cursor.fetchall() is None:
        return False
    return True


def check_salt_exist(salt):
    cursor = get_users_database_cursor()
    sql = "SELECT * from Grouplist where Password = '%s'" % (salt)
    cursor.execute(sql)
    if cursor.fetchall() is None:
        return False
    else:
        return True


def check_in_team(course, username):
    cursor = get_users_database_cursor()
    sql = "SELECT * from Grouplist where instr(Membernames, '-%s-') > 0 and Classname = '%s';" % (username, course)
    cursor.execute(sql)
    fetched = cursor.fetchone()
    if fetched is None:
        return False
    else:
        return True


def add_team_to_database(course, name, groupname, number, teamid):
    cursor = get_users_database_cursor()
    if check_in_team(course, name) is True:
        return "Already in a team"
    else:
        sql = "INSERT into Grouplist (Classname,Groupname,Membernumber,Leadername,Password,Membernames) VALUES ('%s','%s',%s,'%s','%s','-%s-')" % (
        course, groupname, number, name, teamid, name)
        cursor.execute(sql)


def add_student_to_team(course, name, teamid):
    cursor = get_users_database_cursor()
    if check_in_team(course, name) is True:
        return "Already in a team"
    sql = "SELECT Membernames from Grouplist where Password = '%s'" % (teamid)
    cursor.execute(sql)
    fetched = cursor.fetchone()
    if fetched is None:
        return "No such group has this id"
    else:
        fetched = fetched[0]
        fetched = fetched + name + '-'
        sql = "UPDATE Grouplist set Membernames = '%s' where Password = '%s'" % (fetched, teamid)
        cursor.execute(sql)


def show_user():
    cursor = get_users_database_cursor()
    sql = "select * FROM Grouplist"
    cursor.execute(sql)
    return cursor.fetchall()


def drop_all():
    cursor = get_users_database_cursor()
    sql = "DELETE from Grouplist"
    cursor.execute(sql)


if __name__ == '__main__':
    add_student_to_team('CS101', 'Zhao', '1234123')
    print(show_user())
