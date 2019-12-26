import os
import sqlite3


def get_classes_database_cursor():
    conn = sqlite3.connect("classes.db")
    conn.isolation_level = None
    return conn.cursor()


def find_teacher_class(username):
    cursor = get_classes_database_cursor()
    sql = "SELECT DISTINCT Classname FROM Classnamelist where Teacherusername = '%s'" % (username)
    cursor.execute(sql)
    fetched = cursor.fetchall()
    if fetched is None:
        print("No classes")
    else:
        teachercourse = []
        for row in fetched:
            teachercourse.append(row[0])
        return teachercourse


def check_homework(course, teacherusername, index):
    indexpath = os.path.join('homework', course, teacherusername, index)
    try:
        file_name_list = os.listdir(indexpath)
        return file_name_list
    except:
        return "None"


def rectify_homework(course, number, filename: str, grade):
    cursor = get_classes_database_cursor()
    sql = "Update Handinhomework set Score = %s where Classname='%s' and username='%s' and homeworkindex = %s" % (
        grade, course, filename, number)
    cursor.execute(sql)
