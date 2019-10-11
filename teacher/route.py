from flask import render_template, redirect, url_for, request, send_from_directory
from app import app, session
import sqlite3
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
from teacher.addplans import addplans
from teacher.addexperience import addexperience

@app.route('/teacher/index')
def teacherindex():
    return render_template("teacher_index.html")


@app.route('/teacher/upload', methods=["GET", "POST"])
def teacherupload():
    if request.method == 'GET':
        return render_template("teacher_upload.html")
    else:
        if 'file' not in request.files:
            return render_template("teacher_upload.html", msg="Upload file failure")
        file = request.files['file']

        if file.filename == '':
            return render_template("teacher_upload.html", msg="Upload file failure")

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("teacher_upload.html", msg="Upload file success")
    return render_template("teacher_upload.html", msg="Upload file failure")


@app.route('/teacher/addplan', methods=["GET", "POST"])
def teacheraddplan():
    if request.method == "GET":
        return render_template("teacher_addplan.html")
    else:
        plandate = request.form.get('plandate')
        plantitle = request.form.get('plantitle')
        plancontent = request.form.get('plancontent')
        if plantitle is "" or plancontent is "" or plancontent is "":
            return render_template("teacher_addplan.html", msg="Add Plan Error")
        addplans(plandate, plantitle, plancontent)
    return render_template("teacher_addplan.html", msg="Add Plan Success")


@app.route('/teacher/addexperience', methods=["GET", "POST"])
def teacheraddexperience():
    if request.method == "GET":
        return render_template("teacher_addplan.html")
    else:
        experiencedate = datetime.date.today()
        experiencetitle = request.form.get('experiencetitle')
        experiencecontent = request.form.get('experiencecontent')
        if experiencetitle is "" or experiencecontent is "":
            return render_template("teacher_addplan.html", msg="Add Plan Error")
        addexperience(experiencedate, experiencetitle, experiencecontent)
        return render_template("teacher_addplan.html", msg="Add Plan Success")
