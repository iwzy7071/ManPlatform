import datetime
import os

from flask import render_template, redirect, url_for, request, send_from_directory, flash

from app import app, session
from student.createteam import check_teacher_course_teams
from teacher.addexperience import addexperience, showusers, showcontents
from teacher.addplans import addplans
from teacher.findteachingplan import find_teacher_homework, find_teacher_plan
from teacher.homework import add_homework
from teacher.introduction import display_teacher_introduction, update_teacher_introduction
from teacher.introduction import show_teacher_name
from teacher.rectify import check_homework, find_teacher_class, rectify_homework
from teacher.seejournal import get_all_messages
from teacher.selectingquestion import add_key_to_account, find_my_key, insert_selecting_question, find_key_whether_exist
from teacher.selectingquestion import find_my_key_in_list, showallquestion, get_all_resources


@app.route('/teacher/index')
def teacherindex():
    return redirect(url_for('teacherrectifyhomework'))


@app.route('/teacher/upload', methods=["GET", "POST"])
def teacherupload():
    if request.method == 'GET':
        message = {'name': session['name']}
        return render_template("teacher_upload.html", message=message)
    else:
        if 'file' not in request.files:
            message = {'name': session['name'], 'messages': "上传文件失败"}
            return render_template("teacher_upload.html", message=message)
        file = request.files['file']

        if file.filename == '':
            message = {'name': session['name'], 'messages': "上传文件失败"}
            return render_template("teacher_upload.html", message=message)

        if file:
            filename = session['name'] + '-' + file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash([2, session['name'], '已上传资料'])
            message = {'name': session['name'], 'messages': "上传成功"}
            return render_template("teacher_upload.html", message=message)
    message = {'name': session['name'], 'messages': "上传文件失败"}
    return render_template("teacher_upload.html", message=message)


@app.route('/teacher/addplan', methods=["GET", "POST"])
def teacheraddplan():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': find_teacher_class(session['name'])}
        return render_template("teacher_addplan.html", message=message)
    else:
        plandate = request.form.get('plandate')
        plantitle = request.form.get('plantitle')
        plancontent = request.form.get('plancontent')
        course = request.form.get('course')
        if plantitle is "" or plancontent is "" or plancontent is "":
            message = {'name': session['name'], 'info': "添加计划失败", 'messages': find_teacher_class(session['name'])}
            return render_template("teacher_addplan.html", message=message)
        addplans(session['name'], course, plandate, plantitle, plancontent)
        flash([2, session['name'], '已添加教学计划'])
    message = {'name': session['name'], 'info': "添加计划成功", 'messages': find_teacher_class(session['name'])}
    return render_template("teacher_addplan.html", message=message)


@app.route('/teacher/showplans', methods=["GET", "POST"])
def teachershowplans():
    if request.method == "GET":
        results = find_teacher_plan(session['name'])
        results = [result[1:] for result in results]
        if len(results) == 0:
            return redirect(url_for("teacheraddplan"))
        message = {'name': session['name'], 'messages': results}
        return render_template("teacher_showplans.html", message=message)


@app.route('/teacher/showhomeworks', methods=["GET", "POST"])
def teachershowhomeworks():
    if request.method == "GET":
        results = list(find_teacher_homework(session['name']))
        results = [list(x[1:]) for x in results]
        for result in results:
            result[-1] = 'True' if result[-1] == 1 else 'False'
            result[4] = result[4][:result[4].index(' ')]
        if len(results) == 0:
            return redirect(url_for("teacherassignhomework"))
        message = {'name': session['name'], 'messages': results}
        return render_template("teacher_showhomework.html", message=message)


@app.route('/teacher/addexperience', methods=["GET", "POST"])
def teacheraddexperience():
    if request.method == "GET":
        message = {'name': session['name']}
        return render_template("teacher_addexperience.html", message=message)
    else:
        experiencedate = datetime.date.today()
        experiencetitle = request.form.get('experiencetitle')
        experiencecontent = request.form.get('experiencecontent')
        if experiencetitle is "" or experiencecontent is "":
            message = {'name': session['name'], 'messages': "添加失败"}
            return render_template("teacher_addexperience.html", message=message)
        addexperience(session['name'], experiencedate, experiencetitle, experiencecontent)
        message = {'name': session['name'], 'messages': "添加成功"}
        return render_template("teacher_addexperience.html", message=message)


@app.route('/teacher/seejournal', methods=["GET", "POST"])
def teacherseejournal():
    message = {'name': session['name'], 'messages': get_all_messages()}
    return render_template("teacher_seejournal.html", message=message)


@app.route('/teacher/addintro', methods=["GET", "POST"])
def teacheraddintro():
    if request.method == "GET":
        message = {'name': session['name']}
        return render_template("teacher_addintro.html", message=message)
    else:
        content = request.form.get('content')
        if content is "":
            message = {'name': session['name'], 'messages': "添加个人介绍失败"}
            return render_template("teacher_addintro.html", message=message)
        update_teacher_introduction(session['name'], content)
        message = {'name': session['name'], 'messages': "更新个人介绍成功"}
        return render_template("teacher_addintro.html", message=message)


@app.route('/teacher/assignhomework', methods=["GET", "POST"])
def teacherassignhomework():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': find_teacher_class(session['name'])}
        return render_template("teacher_homework.html", message=message)
    else:
        course = request.form.get('course')
        title = request.form.get('title')
        content = request.form.get('content')
        ddl = request.form.get('ddl')
        delay = request.form.get('delay')
        number = request.form.get('homenumber')

        if course is "" or title is "" or content is "" or ddl is "":
            message = {'name': session['name'], 'messages': find_teacher_class(session['name']), "info": "作业设置失败"}
            return render_template("teacher_homework.html", message=message)

        coursepath = os.path.join('homework', course)
        print(coursepath)
        if not os.path.exists(coursepath):
            os.makedirs(coursepath)

        dirpath = os.path.join(coursepath, session['name'])

        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)

        homework_path = os.path.join(dirpath, str(number))
        if not os.path.exists(homework_path):
            os.makedirs(homework_path)

        file = request.files['file']
        if file:
            print(os.path.join(homework_path, file.filename))
            file.save(os.path.join(homework_path, file.filename))

        add_homework(session['name'], course, number, title, ddl, datetime.datetime.today(), delay)
        message = {'name': session['name'], 'messages': find_teacher_class(session['name']), "info": "作业设置成功"}
        return render_template("teacher_homework.html", message=message)

    message = {'name': session['name'], 'messages': find_teacher_class(session['name']), "info": "作业设置失败"}
    return render_template("teacher_homework.html", message=message)


@app.route('/teacher/rectifyhomework', methods=["GET", "POST"])
def teacherrectifyhomework():
    if request.method == 'GET':
        if 'button' in session:
            session.pop('button')
        message = {'name': session['name'], 'messages': [0, find_teacher_class(session['name'])]}
        return render_template("teacher_rectify.html", message=message)
    else:
        if 'button' not in session:
            course = request.form.get('course')
            number = request.form.get('number')
            if course == '' or number == '':
                message = {'name': session['name'], 'messages': [0, find_teacher_class(session['name'])]}
                return render_template("teacher_rectify.html", message=message)
            homework = check_homework(course, session['name'], number)
            if homework == "None":
                return redirect(url_for("teacherrectifyhomework"))
            session['button'] = True
            session['homework'] = homework
            session['number'] = number
            session['course'] = course
            message = {'name': session['name'], 'messages': [1, course, number, homework]}
            return render_template('teacher_rectify.html', message=message)
        else:
            session.pop('button')
            workname = request.form.get('workname')
            worknumber = request.form.get('worknumber')
            if worknumber == '':
                return redirect(url_for("teacherrectifyhomework"))
            workname = workname[:workname.index('.')]
            rectify_homework(session['course'], session['number'], workname, worknumber)
            flash([5, session['name'], '已批改' + session['course'] + '作业' + str(session['number'])])
            session.pop('course')
            session.pop('number')
            return redirect(url_for("teacherrectifyhomework"))


@app.route('/teacher/<text>', methods=["GET", "POST"])
def teachershowhomework(text):
    dirname = os.path.join('homework', session['course'], session['name'], session['number'])
    return send_from_directory(dirname, text)


@app.route('/teacher/showteacherintro', methods=["GET", "POST"])
def teachershowteacher():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': [0, show_teacher_name()]}
        print(message)
        return render_template("teacher_showteacher.html", message=message)
    else:
        teacher = request.form.get('teacher')
        message = {'name': session['name'], 'messages': [1, display_teacher_introduction(teacher)]}
        return render_template("teacher_showteacher.html", message=message)


@app.route('/teacher/showteacherexperience', methods=["GET", "POST"])
def teachershowexperience():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': [0, showusers()]}
        return render_template("teacher_showexperience.html", message=message)
    else:
        teacher = request.form.get('teacher')
        if teacher == 'None':
            return redirect(url_for("teachershowexperience"))
        message = {'name': session['name'], 'messages': [1, showcontents(teacher)]}
        return render_template("teacher_showexperience.html", message=message)


@app.route('/teacher/addproblem', methods=["GET", "POST"])
def teacher_addproblem():
    if request.method == "GET":
        if find_my_key_in_list(session['name']) is None:
            return redirect(url_for("teacheraddkey"))

        message = {'name': session['name'],
                   'messages': ['', find_teacher_class(session['name'])], 'keys': find_my_key_in_list(session['name'])}
        return render_template("teacher_addproblem.html", message=message)
    else:
        course = request.form.get('course')
        content = request.form.get('content')
        numberA = request.form.get('numberA')
        numberB = request.form.get('numberB')
        numberC = request.form.get('numberC')
        numberD = request.form.get('numberD')
        numberTrue = request.form.get('numberTrue')
        keychoose = request.form.get('keychoose')
        if course is '' or content is '' or numberA is '' or numberB is '' or numberC is '' or numberD is '' or numberTrue is '' or keychoose is '':
            message = {'name': session['name'], 'messages': ['问题输入不能为空', find_teacher_class(session['name'])],
                       'keys': find_my_key_in_list(session['name'])}
            return render_template("teacher_addproblem.html", message=message)
        if find_my_key(session['name']) is None:
            message = {'name': session['name'], 'messages': ['请先设置KEY值', find_teacher_class(session['name'])],
                       'keys': find_my_key_in_list(session['name'])}
            return render_template("teacher_addproblem.html", message=message)
        print(keychoose)
        insert_selecting_question(session['name'], course,
                                  content, numberA + '-' + numberB + '-' + numberC + '-' + numberD, numberTrue,
                                  keychoose)
        message = {'name': session['name'], 'messages': ['添加作业成功', find_teacher_class(session['name'])],
                   'keys': find_my_key_in_list(session['name'])}
    return render_template("teacher_addproblem.html", message=message)


@app.route('/teacher/addkey', methods=["GET", "POST"])
def teacheraddkey():
    if request.method == "GET":
        message = {'name': session['name'], 'key': find_my_key_in_list(session['name'])}
        return render_template("teacher_generate_key.html", message=message)
    else:
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 == '' or password2 == '':
            message = {'name': session['name'], 'messages': '密钥不能为空'}
            return render_template("teacher_generate_key.html", message=message)
        if password1 != password2:
            message = {'name': session['name'], 'messages': '密钥不匹配'}
            return render_template("teacher_generate_key.html", message=message)
        add_key_to_account(session['name'], password1)
        message = {'name': session['name'], 'messages': '添加密钥成功'}
    return render_template("teacher_generate_key.html", message=message)


@app.route('/teacher/receivekey', methods=["GET", "POST"])
def teacherreceivekey():
    if request.method == "GET":
        message = {'name': session['name']}
        return render_template("teacher_receive_key.html", message=message)
    else:
        password = request.form.get('password')
        if password == '':
            message = {'name': session['name'], 'messages': '密钥不能为空'}
            return render_template("teacher_generate_key.html", message=message)
        if not find_key_whether_exist(password):
            message = {'name': session['name'], 'messages': '密钥不存在'}
            return render_template("teacher_receive_key.html", message=message)

    add_key_to_account(session['name'], password)
    message = {'name': session['name'], 'messages': '添加密钥成功'}
    return render_template("teacher_receive_key.html", message=message)


@app.route('/teacher/showproblem', methods=["GET", "POST"])
def teacher_showproblem():
    questions = showallquestion(session['name'])
    if questions is False:
        return redirect(url_for("teacher_addproblem"))
    result = []
    for question in questions:
        print(question)
        answer = question[4].split('-')
        result += [[question[0], question[1], question[2], question[3], answer[0], answer[1], answer[2], answer[3],
                    question[5], question[6]]]
    message = {'name': session['name'], 'messages': result}
    return render_template("teacher_showproblems.html", message=message)


@app.route('/teacher/showresource', methods=["GET", "POST"])
def teacher_showresource():
    if len(get_all_resources(session['name'])) == 0:
        return redirect(url_for("teacherupload"))
    message = {'name': session['name'], 'messages': get_all_resources(session['name'])}
    return render_template("teacher_see_resource.html", message=message)


@app.route('/deleteresource/<filename>', methods=["GET", "POST"])
def teacher_deleteresource(filename):
    path = os.path.join('/root/software/uploadfiles', session['name'] + '-' + filename)
    os.remove(path)
    return redirect(url_for('teacher_showresource'))


@app.route('/downloadresource/<filename>', methods=["GET", "POST"])
def teacher_downloadresource(filename):
    print(session['name'] + '-' + filename)
    return send_from_directory('uploadfiles', filename=session['name'] + '-' + filename)


@app.route('/teacher/showteams', methods=["GET", "POST"])
def teacher_showteams():
    groups = check_teacher_course_teams(session['name'])
    result = []
    for group in groups:
        group = [group[0], group[1], group[2], group[3], group[4]]
        result += [group]
    message = {'name': session['name'], 'messages': result}
    return render_template("teacher_showteams.html", message=message)
