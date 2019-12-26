from flask import render_template, redirect, url_for, request

from admin.pinboard import create_pinboard
from app import app, session
from login.findpassword import check_answer_to_question, rectify_password
from login.login import redirect_page_type, get_correct_password, get_user_type


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'name' in session and 'type' in session:
        return redirect(url_for(redirect_page_type(session['type'])))
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get('login')
        password = request.form.get('password')

        try:
            correct_password = get_correct_password(request.form.get('login'))[0]
        except:
            return render_template("login.html", message="密码错误")

        if correct_password is not None and correct_password == password:
            session['name'] = username
            user_type = get_user_type(username)[0]
            session['type'] = user_type
            return redirect(url_for(redirect_page_type(user_type)))
        return redirect(url_for("login"))


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        text = request.form.get('text')
        create_pinboard(text)
        return render_template("index.html", message="已成功留言")


@app.route('/logout')
def logout():
    # if not login, then refer it to the original index
    if 'name' not in session or 'type' not in session:
        return redirect(request.referrer)
    session.pop('name')
    session.pop('type')
    return redirect(url_for('index'))


@app.route('/findpassword', methods=["GET", "POST"])
def findpassword():
    if request.method == 'GET':
        return render_template("findpassword.html")
    else:
        username = request.form.get('login')
        question = request.form.get('question')
        answer = request.form.get('answer')
        password = request.form.get('password')
        if check_answer_to_question(username, question, answer):
            rectify_password(username, password)
            message = "修改密码成功"
        else:
            message = "密保问题回答错误"
        return render_template("findpassword.html", message=message)
