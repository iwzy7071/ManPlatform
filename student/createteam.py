import random
import sqlite3
import string

from student.uploadhomework import find_student_teacher


def get_teamid():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    while (check_salt_exist(salt)):
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return salt


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

    if cursor.fetchall() is not None:
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
        return False
    else:
        fetched = fetched[0]
        fetched = fetched + name + '-'
        sql = "UPDATE Grouplist set Membernames = '%s' where Password = '%s'" % (fetched, teamid)
        cursor.execute(sql)
    return True


def show_user():
    cursor = get_users_database_cursor()
    sql = "select * FROM Grouplist"
    cursor.execute(sql)
    return cursor.fetchall()


def drop_all():
    cursor = get_users_database_cursor()
    sql = "DELETE from Grouplist"
    cursor.execute(sql)


def check_teacher_course_teams(username):
    cursor = get_users_database_cursor()
    sql = "SELECT * from Grouplist;"
    cursor.execute(sql)
    groups = cursor.fetchall()
    result = []
    for group in groups:
        course, student = group[0], group[3]
        teacher = find_student_teacher(student, course)[0]
        if teacher == username:
            result += [group]
    return result


if __name__ == '__main__':
    check_teacher_course_teams()
