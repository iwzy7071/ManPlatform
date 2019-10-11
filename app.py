from flask import Flask, render_template, session

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploadfiles'
app.secret_key = 'fba!u?%b*fa89ib%ab^21312/f'