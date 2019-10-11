from flask import render_template, redirect, url_for, request, escape
from app import app, session
from admin.addusers import addusers, findusers,findusertype
from admin.pinboard import get_all_messages
from admin.journal import create_journal
@app.route('/admin/index')
def adminindex():
    return render_template("admin_index.html")


@app.route('/admin/adduser', methods=["GET", "POST"])
def adminaddusers():
    if request.method == 'GET':
        return render_template("admin_adduser.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        usertype = request.form.get('usertype')
        if findusers(username):
            return render_template("admin_adduser.html", msg="Username already exists")
        try:
            addusers(username, password, findusertype(usertype))
        except:
            return render_template("admin_adduser.html", msg="Error Insert")
    return render_template("admin_adduser.html", msg="Success Insert")


@app.route('/admin/pinboard', methods=["GET", "POST"])
def adminpinboard():
    if request.method == 'GET':
        messages = get_all_messages()
        return render_template("admin_pinboard.html", messages = messages)
    else:
        pass
        # Todo: Finish pinboard function: sendMessage and Delete Message


@app.route('/admin/addjournal', methods=["GET", "POST"])
def adminjournal():
    if request.method == 'GET':
        return render_template("admin_addjournal.html")
    else:
        journal = request.form.get('journal')
        create_journal(journal)
    return render_template("admin_addjournal.html", msg="Success Insert")


