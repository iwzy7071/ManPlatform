from flask import Flask,session

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploadfiles'
app.secret_key = 'fba!u?%b*fa89ib%ab^21312/f'

# Flash 0 refers to Administor
# Flash 1 refers to Teacher
# Flash 2 refers to Student
# Flash 3 refers to
# Flash 4 refers to Internal Administor
# Flash 5 refers to Internal Student
