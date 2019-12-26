import os
import shutil
import sqlite3
import time
from email.header import Header
from email.mime.text import MIMEText
from os.path import join
from smtplib import SMTP_SSL

import pandas
import pandas.io.sql as sql


class Email:
    def __init__(self, mail_titile: str, mail_content: str, username: str):
        self.host_server = 'smtp.qq.com'
        self.sender_qq = '2590654152@qq.com'
        self.pwd = 'vubbzmbghryaecgc'
        self.sender_qq_mail = '2590654152@qq.com'
        self.receiver = username
        self.mail_content = mail_content
        self.mail_title = mail_titile

    def send(self):
        smtp = SMTP_SSL(self.host_server)
        smtp.set_debuglevel(1)
        smtp.ehlo(self.host_server)
        smtp.login(self.sender_qq, self.pwd)
        msg = MIMEText(self.mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(self.mail_title, 'utf-8')
        msg["From"] = self.sender_qq_mail
        msg["To"] = self.receiver
        smtp.sendmail(self.sender_qq_mail, self.receiver, msg.as_string())
        smtp.quit()


def backupfunction():
    backupdirectory = "/root/software/backup/"
    today = time.strftime('%Y-%m-%d')  # -%H-%M-%S
    todaydirectory = backupdirectory + today
    if not os.path.exists(todaydirectory):
        os.makedirs(todaydirectory)
    os.system('cp /root/software/users.db %s' % (todaydirectory))
    os.system('cp /root/software/classes.db %s' % (todaydirectory))
    os.system('cp /root/software/questions.db %s' % (todaydirectory))


def send_Info_Email(username):
    title = "Boooya邮件提示信息"
    content = "尊敬的管理员，您的账号%s于%s时间将数据库导出，请您知晓。" % (username, time.strftime('%Y-%m-%d %H:%M:%S'))
    mail = Email(title, content, username)
    mail.send()


def send_Danger_Email(username):
    title = "Boooya紧急安全事件"
    content = "尊敬的管理员，我们检测到你的网站www.boooya.top于%s疑似遭到攻击，已经为您将数据库备份" % (time.strftime('%Y-%m-%d %H:%M:%S'))
    mail = Email(title, content, username)
    mail.send()


def loadin_csv():
    conn = sqlite3.connect("dbname.db")
    df = pandas.read_csv('d:\\filefolder\csvname.csv')


def traverse_db(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("select name from sqlite_master where type='table' order by name")
    tables = cur.fetchall()
    for table_name in tables:
        table = sql.read_sql('select * from {}'.format(table_name[0]), conn)
        table.to_csv(join('/root/software/save_data', "{}.csv").format(table_name[0]))


def output_csv():
    shutil.rmtree('save_data')
    os.mkdir('save_data')
    db_names = ['users.db', 'classes.db', 'questions.db']
    for db_name in db_names:
        traverse_db(db_name)
