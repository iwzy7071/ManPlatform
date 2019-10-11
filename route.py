from app import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages-404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('pages-404.html')

from flask import render_template
from login import route
from teacher import route
from student import route
from admin import route
from visiter import route





if __name__ == '__main__':
    app.run()
