#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_wtf import Form
from flask import Flask,render_template,flash,redirect,url_for,session,request ,logging
from wtforms import StringField,TextAreaField,validators,TextField,SubmitField
import MySQLdb
import schedule
import time
import smtplib
from email.mime.text import MIMEText

app=Flask(__name__)


class ContactForm(Form):
    name = TextField("Name")
    email = TextField("Email")
    msg = TextAreaField("Message")
    submit = SubmitField("Submit")
    telephone=TextField("Telephone")



@app.route('/')
def index():
    db = MySQLdb.connect("127.0.0.1", "root", "", "DATA", charset='utf8')
    cur = db.cursor()

    cur.execute("""SELECT * FROM Posts WHERE cat_fk='0'""")
    posts1 = cur.fetchall()

    cur.execute("""SELECT * FROM Posts WHERE cat_fk='1'""")
    posts2 = cur.fetchall()
    return render_template('home.html', posts1=posts1,posts2=posts2)

def send_Email(name,mail,phone,msg):
    print("send the email")
    print(name)
    print(mail)
    print(phone)
    print(msg)
    the_MSG=name+"\n"+mail+"\n"+phone+"\n"+msg
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login("islam.awadallah84@gmail.com", "11317784")
    server.sendmail(mail,"islam.awadallah84@gmail.com", the_MSG)
    server.quit()


@app.route('/search',methods=["GET", "POST"])
def search():
    pos=""
    db = MySQLdb.connect("127.0.0.1", "root", "", "DATA", charset='utf8')
    cur = db.cursor()

    user=""
    if request.method=='POST':
        user=request.form.get('Search')

        # print("THE USSSSSSSSSSSSSER ======>",user)


    try:
        cur.execute(""" SELECT * FROM Posts where post_msg like '% """ + user + """ %' """ )

        pos = cur.fetchall()
        print(cur)
        print(pos)
        print("islam")
    except:
        print("NOO")



    return render_template('search.html',pos=pos)

@app.route('/contact',methods=["GET", "POST"])
def contact():
    if request.method=='POST':
        Uname=request.form.get('Name')
        Umail = request.form.get('Email')
        Uphone = request.form.get('Telephone')
        Umsg = request.form.get('message')

        send_Email(Uname,Umail,Uphone,Umsg)
    form = ContactForm()

    if request.method == 'POST':
        return 'Form posted'

    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    db = MySQLdb.connect("127.0.0.1", "root", "", "DATA", charset='utf8')
    cur = db.cursor()

    cur.execute("""SELECT * FROM Posts""")
    posts = cur.fetchall()

    return render_template('products.html',posts=posts)

@app.route('/laptop')
def laptop():
    db = MySQLdb.connect("127.0.0.1", "root", "", "DATA", charset='utf8')
    cur = db.cursor()

    cur.execute("""SELECT * FROM Posts WHERE cat_fk='0'""")
    lap = cur.fetchall()

    return render_template('laptop.html',lap=lap)



# def job():
#     app.secret_key = 'secret123'
#     app.run(debug=True)

@app.route('/phones')
def phones():
    db = MySQLdb.connect("127.0.0.1", "root", "", "DATA", charset='utf8')
    cur = db.cursor()

    cur.execute("""SELECT * FROM Posts WHERE cat_fk='1'""")
    pho = cur.fetchall()
    return render_template('phones.html',pho=pho)




@app.route('/sime')
def sime():
    db = MySQLdb.connect("127.0.0.1", "root", "", "DATA", charset='utf8')
    cur = db.cursor()

    cur.execute("""SELECT * FROM Simelarity""")
    si = cur.fetchall()
    return render_template('sime.html',si=si)

if __name__=='__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
    # app.secret_key = 'secret123'
    # app.run(debug=True)

    # schedule.every(0.1).minutes.do(job)
    #
    # while 1:
    #     schedule.run_pending()
    #     time.sleep(1)
