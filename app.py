from flask import Flask,request, url_for, redirect, render_template
import pandas as pd
import pickle
import numpy as np
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route('/note')
def note():
	return render_template('notebook.html')


@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    number = request.args.get('mobile','')
    email = request.args.get('email','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    sid = SentimentIntensityAnalyzer()
    if request.method == 'POST':
        text = request.form['message']
        data = [text]
        score = sid.polarity_scores(data)
        if score['compound'] > 0:
            prediction = 1
        else:
            prediction = 0
            
        if prediction == 0:
            return render_template('result.html',pred=f'Negative')
        elif prediction == 1:
            return render_template('result.html',pred=f'Positive')


@app.route('/index')
def index():
	return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)