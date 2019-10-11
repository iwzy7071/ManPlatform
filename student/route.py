from flask import render_template, redirect, url_for, request, escape
from app import app, session
from student.studentprotection import find_student_protection, add_student_protection


def get_answer_type(type: str) -> int:
    if type == "您最喜欢的明星是":
        return 0
    if type == "您最喜欢的老师是":
        return 1
    if type == "您最喜欢的课程是":
        return 2
    if type == "您最喜欢的食物是":
        return 3
    if type == "您最喜欢的朋友是":
        return 4


@app.route('/student/index')
def studentindex():
    if not find_student_protection(session['name']):
        return redirect(url_for("studentprotection"))
    return render_template("student_index.html")


@app.route('/student/protection', methods=["GET", "POST"])
def studentprotection():
    if request.method == 'GET':
        return render_template("student_protection.html")
    else:
        question = request.form.get("question")
        content = request.form.get('content')
        verify = request.form.get('verify')
        print(question, content, verify)
        if content is "" or verify is "":
            return render_template("student_protection.html", msg="输入不能为空")
        if content != verify:
            return render_template("student_protection.html", msg="两次输入不一致")
        add_student_protection(get_answer_type(question), content, session['name'])
        return redirect(url_for("studentindex"))


@app.route('/student/seejournal', methods=["GET", "POST"])
def adminjournal():
    if request.method == 'GET':
        return render_template("admin_addjournal.html")
    else:
        journal = request.form.get('journal')
        create_journal(journal)
    return render_template("admin_addjournal.html", msg="Success Insert")

# Todo: Finish seeing journal functions for student and teachers
