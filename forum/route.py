from flask import render_template, redirect, url_for, request

from app import app
from forum.forum import get_message, send_message


@app.route('/forum', methods=["GET", "POST"])
def forum():
    if request.method == "GET":
        message = {'messages': get_message()}
        return render_template('forum.html', message=message)
    else:
        message = request.form.get('message')
        send_message(message)
        return redirect(url_for('forum'))
