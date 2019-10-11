from flask import render_template, redirect, url_for, request, escape
from app import app, session
import sqlite3
from werkzeug.security import check_password_hash
import os

def get_database_cursor():
    conn = sqlite3.connect("users.db")
    print(os.system("pwd"))
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


def redirect_page_type(type:str):
    if int(type) == 0:
        return "teacherindex"
    if int(type) == 1:
        return "studentindex"
    if int(type) == 2:
        return "visitorindex"
    if int(type) == 3:
        return "adminindex"
    raise Exception("Wrong UserType!")


# the login function involves the users.db
# the user.db contains User Table
# Three Attributes in User Table: Name \ Password \ Type
# Note that Type 0 refers to Teacher \ Type 1 refers to Student
# Type 2 refers to visitor \ Type 4 refers to admin
@app.route('/login', methods=["GET", "POST"])
def login():
    if 'name' in session and 'type' in session:
        # ToDo: redirect Different pages according to User Type
        return redirect(url_for(redirect_page_type(session['type'])))

    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get('login')
        password = request.form.get('password')

        try:
            correct_password = get_correct_password(request.form.get('login'))[0]
        except:
            return redirect(url_for("login"))

        if correct_password is not None and correct_password == password:
            session['name'] = username
            user_type = get_user_type(username)[0]
            session['type'] = user_type
            return redirect(url_for(redirect_page_type(user_type)))
        return redirect(url_for("login"))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/logout')
def logout():
    # if not login, then refer it to the original index
    if 'name' not in session or 'type' not in session:
        return redirect(request.referrer)
    session.pop('name')
    session.pop('type')
    return redirect(url_for('index'))