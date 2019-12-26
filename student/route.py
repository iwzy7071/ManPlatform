import datetime
import os

from flask import render_template, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename

from admin.course import show_class, show_specific_class, show_person_class
from app import app, session
from student.calculatingaverage import calculate_average_new
from student.checkid import check_team_name, check_in_team, check_member_id, get_member_id
from student.createteam import get_teamid, add_student_to_team, add_team_to_database
from student.downloadfiles import get_all_files
from student.pathtable import add_path, find_path
from student.seejournal import get_all_messages
from student.selectingquestion import find_any_question
from student.studentprotection import find_student_protection, add_student_protection
from student.uploadhomework import find_student_class, find_student_teacher, add_homework_in_database
from teacher.addexperience import showusers, showcontents
from teacher.findteachingplan import find_student_homework
from teacher.introduction import display_teacher_introduction, show_teacher_name


@app.route('/student/index')
def studentindex():
    if not find_student_protection(session['name']):
        return redirect(url_for("studentprotection"))
    return redirect(url_for("studentuploadhomework"))


@app.route('/student/protection', methods=["GET", "POST"])
def studentprotection():
    if request.method == 'GET':
        return render_template("student_protection.html")
    else:
        question = request.form.get("question")
        content = request.form.get('content')
        verify = request.form.get('verify')
        if content is "" or verify is "":
            message = {'name': session['name'], 'messages': "输入不能为空"}
            return render_template("student_protection.html", message=message)
        if content != verify:
            message = {'name': session['name'], 'messages': "两次输入不一致"}
            return render_template("student_protection.html", message=message)
        add_student_protection(question, content, session['name'])
        return redirect(url_for("studentuploadhomework"))


@app.route('/student/seejournal', methods=["GET", "POST"])
def studentseejournal():
    message = {'name': session['name'], 'messages': get_all_messages()}
    return render_template("student_seejournal.html", message=message)


@app.route('/student/download_teachers', methods=["GET", "POST"])
def studentdownloadchoose_course():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': find_student_class(session['name'])}
        return render_template("student_show_download.html", message=message)
    else:
        course = request.form.get('course')
        find_student_teacher(session['name'], course)
        return redirect(url_for("studentdownloadchoose", course=course))


@app.route('/courses/<course>', methods=["GET", "POST"])
def studentdownloadchoose(course):
    if request.method == "GET":
        teacher = find_student_teacher(session['name'], course)[0]
        files = get_all_files()
        result = []

        for file in files:
            if file[:file.index('-')] == teacher:
                result.append(file[file.index('-') + 1:])
        session['teacher'] = teacher
        message = {'name': session['name'], 'messages': result}
        return render_template("student_download.html", message=message)


@app.route('/downloadfiles/<filename>', methods=["GET", "POST"])
def downloadfiles(filename):
    return send_from_directory('uploadfiles', session['teacher'] + '-' + filename)


@app.route('/student/showintro', methods=["GET", "POST"])
def studentshowteacher():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': [0, show_teacher_name()]}
        return render_template("student_showteacher.html", message=message)
    else:
        teacher = request.form.get('teacher')
        message = {'name': session['name'], 'messages': [1, display_teacher_introduction(teacher)]}
        return render_template("student_showteacher.html", message=message)


@app.route('/student/uploadhomework', methods=["GET", "POST"])
def studentuploadhomework():
    if request.method == 'GET':
        if 'button' in session:
            session.pop('button')
        if 'info' in session:
            message = {'name': session['name'], 'messages': find_student_class(session['name']),
                       'info': session['info']}
            session.pop('info')
        else:
            message = {'name': session['name'], 'messages': find_student_class(session['name'])}
        return render_template("student_uploadhomework.html", message=message)
    else:
        if 'button' not in session:
            course = request.form.get('course')
            session['course'] = course
            session['button'] = 'true'
            session['teacher'] = find_student_teacher(session['name'], course)
            if not session['teacher']:
                message = {'name': session['name'], 'messages': find_student_class(session['name'])}
                return render_template("student_uploadhomework.html", message=message)
            message = {'name': session['name'], 'messages': [course, session['teacher']]}
            return render_template("student_uploadhomework.html", message=message)
        else:
            course = session['course']
            teacher = session['teacher']
            homenumber = request.form.get('homenumber')
            content = request.form.get('input')
            file = request.files['file']
            homework_path = os.path.join('homework', course, str(teacher[0]), homenumber)
            if file:
                filename = secure_filename(file.filename)
                print(filename)
                if filename != 'zip':
                    session['info'] = "回家作业必须以zip格式上传"
                    return redirect(url_for("studentuploadhomework"))
                filename = session['name'] + '.' + filename
                file.save(os.path.join(homework_path, filename))
                add_homework_in_database(course, str(teacher[0]), session['name'], homenumber, content,
                                         datetime.datetime.today())
                session.pop('button')
                session.pop('course')
                session.pop('teacher')
                session['info'] = "上传回家作业成功"
                return redirect(url_for("studentuploadhomework"))
            session['info'] = "上传回家作业失败"
            return redirect(url_for("studentuploadhomework"))


@app.route('/student/createteam', methods=["GET", "POST"])
def studentcreateteam():
    if request.method == 'GET':
        message = {'name': session['name'], 'messages': find_student_class(session['name'])}
        return render_template("student_creategroup.html", message=message)
    else:
        course = request.form.get('course')
        name = request.form.get('name')
        number = request.form.get('number')
        teamid = get_teamid()
        message = {'name': session['name'], 'messages': [find_student_class(session['name'])], 'info': teamid}
        add_team_to_database(course, session['name'], name, number, teamid)
        return render_template("student_creategroup.html", message=message)


@app.route('/student/jointeam', methods=["GET", "POST"])
def studentjointeam():
    if request.method == 'GET':
        message = {'name': session['name'], 'messages': find_student_class(session['name'])}
        return render_template("student_joingroup.html", message=message)
    else:
        course = request.form.get('course')
        teamid = request.form.get('teamid')

        if check_in_team(course, session['name']):
            message = {'name': session['name'],
                       'messages': [find_student_class(session['name']), '已经在一个队伍中']}
            return render_template("student_joingroup.html", message=message)
        if add_student_to_team(course, session['name'], teamid):
            message = {'name': session['name'],
                       'messages': [find_student_class(session['name']), '成功加入队伍']}
            return render_template("student_joingroup.html", message=message)
        message = {'name': session['name'],
                   'messages': [find_student_class(session['name']), '错误队伍ID']}
        return render_template("student_joingroup.html", message=message)


@app.route('/student/showcourse', methods=["GET", "POST"])
def studentshowcourse():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': ['0', show_class()]}
        return render_template("student_showcourse.html", message=message)
    else:
        coursename = request.form.get('course')
        message = {'name': session['name'], 'messages': [1, show_specific_class(coursename)]}
        print(message.get('messages'))
        return render_template("student_showcourse.html", message=message)


@app.route('/student/showteacherexperience', methods=["GET", "POST"])
def studentshowexperience():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': [0, showusers()]}
        return render_template("student_showteacherexperience.html", message=message)
    else:
        teacher = request.form.get('teacher')
        if teacher == 'None':
            return redirect(url_for("studentshowexperience"))
        message = {'name': session['name'], 'messages': [1, showcontents(teacher)]}
        return render_template("student_showteacherexperience.html", message=message)


@app.route('/student/showteamid', methods=["GET", "POST"])
def studentshowteamid():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': [0, show_person_class(session['name'])]}
        return render_template("student_showteamid.html", message=message)
    else:
        course = request.form.get('course')
        if course == 'None':
            return redirect(url_for("studentshowteamid"))
        message = {'name': session['name'], 'messages': [1, check_team_name(course, session['name'])]}
        return render_template("student_showteamid.html", message=message)


@app.route('/student/showmemberid', methods=["GET", "POST"])
def studentshowmemberid():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': [0, show_person_class(session['name'])]}
        return render_template("student_showmemberid.html", message=message)
    else:
        course = request.form.get('course')
        if course == 'None':
            return redirect(url_for("studentshowteamid"))
        if check_member_id(course, session['name']):
            message = {'name': session['name'], 'messages': [1, get_member_id(course, session['name'])]}
            return render_template("student_showmemberid.html", message=message)
        message = {'name': session['name'], 'messages': [2, "不在队伍内"]}
        return render_template("student_showmemberid.html", message=message)


@app.route('/student/showscore', methods=["GET", "POST"])
def studentshowscore():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': [0, show_person_class(session['name'])]}
        return render_template("student_score.html", message=message)
    else:
        course = request.form.get('course')
        if course is None:
            return redirect(url_for("studentshowscore"))
        message = {'name': session['name'], 'messages': [1, calculate_average_new(session['name'], course)]}
        return render_template("student_score.html", message=message)


@app.route('/student/choosethecourse', methods=["GET", "POST"])
def studentchooseproblem():
    if request.method == "GET":
        message = {'name': session['name'], 'messages': [0, show_person_class(session['name'])]}
        return render_template("student_choose_problem.html", message=message)
    else:
        course = request.form.get('course')

        return redirect(url_for('studentanswerproblem', course=course))


@app.route('/student/<course>', methods=["GET", "POST"])
def studentanswerproblem(course):
    if request.method == "GET":
        session['course'] = course
        content = find_any_question(session['course'])
        problem, choice, answer = content[3], content[4].split('-'), content[5]
        message = {'name': session['name'], 'messages': [0, problem, choice, answer]}
        session['answer'] = answer
        return render_template("student_answer_problem.html", message=message)
    else:
        rchoice = request.form.get('choice')
        content = find_any_question(session['course'])
        problem, choice, answer = content[3], content[4].split('-'), content[5]
        if rchoice == session['answer']:
            message = {'name': session['name'], 'messages': [0, problem, choice, answer], 'reflection': '回答正确'}
        else:
            message = {'name': session['name'], 'messages': [0, problem, choice, answer], 'reflection': '回答错误'}
        return render_template("student_answer_problem.html", message=message)


@app.route('/student/sharefile', methods=["GET", "POST"])
def studentsharefile():
    if request.method == 'GET':
        message = {'name': session['name']}
        return render_template("student_sharefile.html", message=message)
    else:
        file = request.files['file']
        if file:
            homework_path = os.path.join('share_dir', file.filename)
            file.save(homework_path)
            message = {'name': session['name'], "messages": "文件密钥号" + add_path(homework_path)}
            return render_template("student_sharefile.html", message=message)
        message = {'name': session['name'], "messages": "分享失败"}
        return render_template("student_sharefile.html", message=message)


@app.route('/student/getsharefile', methods=["GET", "POST"])
def studentgetsharefile():
    if request.method == 'GET':
        message = {'name': session['name']}
        return render_template("student_getsharefile.html", message=message)
    else:
        key = request.form.get('KEY')
        filepath = find_path(key)
        if filepath is None:
            message = {'name': session['name'], 'messages': "输入的文件KEY不存在"}
            return render_template("student_getsharefile.html", message=message)
        filename = filepath.split('/')[-1]
        return redirect(url_for("getsharedfiles", filename=filename))


@app.route('/sharedfiles/<filename>', methods=["GET", "POST"])
def getsharedfiles(filename):
    return send_from_directory('share_dir', filename)


@app.route('/student/showhomeworks', methods=["GET", "POST"])
def studentshowhomeworks():
    if request.method == "GET":
        results = find_student_homework(session['name'])
        results = [list(result)[:-1] for result in results]
        for result in results:
            result[5] = result[5][:result[5].index(' ')]
        session['file'] = {}
        for result in results:
            path = os.path.join('/root/software/homework/', result[1], result[0], str(result[2]))
            try:
                file_name = os.listdir(path)[0]
                file_path = path.replace('/', '-')
                result += [file_name]
                session['file'].update({file_name: file_path})
            except:
                result += ['Empty']
        message = {'name': session['name'], 'messages': results}
        return render_template("student_showhomework.html", message=message)


@app.route('/homework/<filename>', methods=["GET", "POST"])
def gethomeworkfile(filename):
    filepath = session['file'][filename]
    filepath = filepath.replace('-', '/')
    return send_from_directory(filepath, filename)
