import os

from flask import render_template, redirect, url_for, request, flash, send_from_directory

from admin.addstudentstocourse import check_enrolled_students, check_unenrolled_students, show_course, show_teachers, \
    drop_user_from_course
from admin.addusers import addusers, findusers, findusertype, selectusers, resetusers, deleteusers
from admin.backup import backupfunction, output_csv, send_Danger_Email, send_Info_Email
from admin.course import addusertocourse
from admin.course import find_class, add_class
from admin.journal import create_journal
from admin.pinboard import get_all_messages, delete_pinboard
from app import app, session
from student.seejournal import get_all_messages as get_messages


@app.route('/admin/index')
def adminindex():
    return redirect(url_for('adminaddusers'))


@app.route('/admin/adduser', methods=["GET", "POST"])
def adminaddusers():
    if request.method == 'GET':
        message = {'name': session['name']}
        return render_template("admin_adduser.html", message=message)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        usertype = request.form.get('usertype')
        realname = request.form.get('realname')
        if username.find("-") != -1:
            message = {'name': session['name'], 'messages': "用户名不能含有非法字符"}
            return render_template("admin_adduser.html", message=message)
        if username == "" or password == "" or realname == "":
            message = {'name': session['name'], 'messages': "用户名不能为空"}
            return render_template("admin_adduser.html", message=message)
        if findusers(username):
            message = {'name': session['name'], 'messages': "用户名已经存在"}
            return render_template("admin_adduser.html", message=message)
        try:
            addusers(username, password, findusertype(usertype), realname)
        except:
            message = {'name': session['name'], 'messages': "添加错误"}
            return render_template("admin_adduser.html", message=message)

    message = {'name': session['name'], 'messages': "成功添加"}
    return render_template("admin_adduser.html", message=message)


@app.route('/admin/pinboard', methods=["GET", "POST"])
def adminpinboard():
    message = {'name': session['name'], 'messages': get_all_messages()}
    if len(message.get('messages')) == 0:
        message = {'name': session['name'], 'messages': [1, "目前暂无留言"]}
    return render_template("admin_pinboard.html", message=message)


@app.route('/admin/addjournal', methods=["GET", "POST"])
def adminjournal():
    if request.method == 'GET':
        message = {'name': session['name']}
        return render_template("admin_addjournal.html", message=message)
    else:
        journal = request.form.get('journal')
        if len(journal) > 500:
            message = {'name': session['name'], 'messages': "添加失败"}
            return render_template("admin_addjournal.html", message=message)
    create_journal(journal)
    flash([0, session['name'], journal])
    message = {'name': session['name'], 'messages': "成功添加"}
    return render_template("admin_addjournal.html", message=message)


@app.route('/deletemessages/<text>', methods=["GET", "POST"])
def deletemessages(text):
    delete_pinboard(text)
    return redirect(url_for("adminpinboard"))


@app.route('/admin/addusertocourse', methods=["GET", "POST"])
def adminusertocourse():
    if request.method == 'GET':
        if 'button' in session:
            session.pop('button')
        message = {'name': session['name'], 'messages': [show_course(), show_teachers()]}
        return render_template("admin_addsturtocourse.html", message=message)
    else:
        if 'button' not in session:
            course = request.values.get('course')
            teacher = request.values.get('teacher')
            session['course'] = course
            session['teacher'] = teacher
            session['button'] = 'true'
            session['student'] = check_enrolled_students(course, teacher)
            message = {'name': session['name'],
                       'messages': [[[session['course']]], [[session['teacher']]],
                                    check_enrolled_students(course, teacher),
                                    check_unenrolled_students(course, teacher)]}
            return render_template("admin_addsturtocourse.html", message=message)
        else:
            student = request.form.getlist('student')
            drop_student = list(set(session['student']) - set(student))
            addusertocourse(session['course'], session['teacher'], student)
            drop_user_from_course(session['course'], drop_student)
            session.pop('course')
            session.pop('teacher')
            session.pop('button')
            return redirect(url_for("adminusertocourse"))


@app.route('/admin/addcourse', methods=["GET", "POST"])
def adminaddcourse():
    if request.method == 'GET':
        message = {'name': session['name']}
        return render_template("admin_addcourse.html", message=message)
    else:
        classname = request.form.get('classname')
        weeklytime = request.form.get('weeklytime')
        introduction = request.form.get('introduction')
        teachingplan = request.form.get('teachingplan')
        requirement = request.form.get('requirement')
        gradingpolicy = request.form.get('gradingpolicy')
        if len(classname) > 150 or len(weeklytime) > 150 or len(introduction) > 150 or len(teachingplan) > 150 or len(
                requirement) > 150 or len(gradingpolicy) > 150:
            message = {'name': session['name'], 'messages': "输入过长"}
            return render_template("admin_addcourse.html", message=message)
            if classname == '' or weeklytime == '' or introduction == '' or teachingplan == '' or requirement == '' or gradingpolicy == '':
                message = {'name': session['name'], 'messages': "输入不能为空"}
                return render_template("admin_addcourse.html", message=message)
        if find_class(classname):
            message = {'name': session['name'], 'messages': "班级名称已经存在"}
            return render_template("admin_addcourse.html", message=message)
        flash([0, session['name'], '添加了 ' + classname + ' 课程'])
        add_class(classname, weeklytime, introduction, teachingplan, requirement, gradingpolicy)
    message = {'name': session['name'], 'messages': "成功添加课程"}
    return render_template("admin_addcourse.html", message=message)


@app.route('/admin/savedatabase', methods=["GET", "POST"])
def adminsavedatabase():
    if request.method == 'GET':
        message = {'name': session['name']}
        return render_template("admin_save_database.html", message=message)
    else:
        password = request.form.get('password')
        if password != '123456':
            message = {'name': session['name'], 'messages': "密码错误"}
            return render_template("admin_save_database.html", message=message)
    backupfunction()
    send_Danger_Email(session['name'])
    message = {'name': session['name'], 'messages': "成功备份数据库"}
    flash([4, session['name'], '备份数据库'])
    return render_template("admin_save_database.html", message=message)


@app.route('/admin/outputexcel', methods=["GET", "POST"])
def adminoutputexl():
    if request.method == 'GET':
        message = {'name': session['name']}
        return render_template("admin_output_exl.html", message=message)
    else:
        password = request.form.get('password')
        if password != '123456':
            message = {'name': session['name'], 'messages': "密码错误"}
            return render_template("admin_output_exl.html", message=message)

    output_csv()
    os.system('zip -r output_data.zip /save_data')
    send_Info_Email()
    return redirect(url_for("outputdata", text="output_data.zip"))


@app.route('/admin/<text>', methods=["GET", "POST"])
def outputdata(text):
    return send_from_directory('.', text)


@app.route('/admin/resetusers', methods=["GET", "POST"])
def adminresetpassword():
    if request.method == 'GET':
        message = {'name': session['name'], 'messages': selectusers()}
        return render_template("admin_reset_password.html", message=message)
    else:
        name = request.form.get('name')
        resetusers(name)
        message = {'name': session['name'], 'messages': selectusers(), 'info': '成功恢复密码'}
        return render_template("admin_reset_password.html", message=message)


@app.route('/admin/seejournal', methods=["GET", "POST"])
def adminseejournal():
    message = {'name': session['name'], 'messages': get_messages()}
    return render_template("admin_seejournal.html", message=message)


@app.route('/admin/deleteusers', methods=["GET", "POST"])
def admindeleteuser():
    if request.method == 'GET':
        message = {'name': session['name'], 'messages': selectusers()}
        return render_template("admin_delete_users.html", message=message)
    else:
        name = request.form.get('name')
        if name == '' or name is None:
            message = {'name': session['name'], 'messages': selectusers(), 'info': '用户名不能为空'}
            return render_template("admin_delete_users.html", message=message)

        deleteusers(name)
        message = {'name': session['name'], 'messages': selectusers(), 'info': '成功删除用户'}
        return render_template("admin_delete_users.html", message=message)
