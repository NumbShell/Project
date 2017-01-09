from flask import Flask, request, url_for, session, render_template, redirect, flash
from functools import wraps
import time
import os
import sqlite3

#Importing my own modules
import _login
import _register


app = Flask(__name__)
app.secret_key = 'some_secret'

#variables
post = ""
g_username = ""

#Establish database
conn = sqlite3.connect('users.db')
c = conn.cursor()


def create_table():
    #Table to store user information.
    c.execute('CREATE TABLE IF NOT EXISTS user(username TEXT, password INT, email TEXT)')

    #Table to store posts.
    c.execute('CREATE TABLE IF NOT EXISTS post(username TEXT, post TEXT, timestamp DATETIME)')

def data_entry():
    pass
    #c.execute("INSERT INTO users VALUES(100, DATETIME('now'), 'Python_', 127)")
    #conn.commit()
    #c.close()
    #conn.close()


@app.route("/logout/")
@_login.login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('home'))


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login/", methods=['GET','POST'])
# Whole login method is coded by Sentdex and modified by me.
def login():
    error = ""
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            #Grab content from database
            username = c.execute("SELECT * FROM user WHERE username=(?)", (attempted_username, ))
            username_data = username.fetchall()

            password = c.execute("SELECT * FROM user WHERE password=(?)", (attempted_password, ))
            password_data = password.fetchall()

            if len(username_data) > 0 and len(password_data) > 0:
                #user = attempted_username
                session['logged_in'] = True
                session['username'] = attempted_username

                flash("You are now logged in")
                return redirect(url_for('home'))
            else:
                flash("Invalid credentials. Try again.")
                #error = "Invalid credentials. Try again."

        return render_template("login.html", error=error)

    except Exception as e:
        return render_template('login.html', error = error)


    return render_template('login.html')

@app.route("/register/", methods=['GET','POST'])
def register():
    return _register.register_required(c, conn)

@app.route("/create_post/", methods=['GET','POST'])
@_login.login_required
def create_post():
    if request.method == "POST":
        notes = request.form['notes']
        global post
        post = notes

        #Add post to database
        try:
            if len(post) > 0:
                c.execute("INSERT INTO post (username, post, timestamp) VALUES(?,?,?)",(session['username'], post, time.strftime("%d/%m/%Y"), ))
                conn.commit()
            else:
                flash("Field is empty")
                return render_template('post.html')
        except:
            conn.rollback()

        #c.close()

        #conn.close()

        return redirect(url_for('board'))

    return render_template('post.html')

@app.route("/community/")
def board():
    global post
    stamp = c.execute("SELECT timestamp FROM post WHERE post=(?)", (post, ))
    data = stamp.fetchall()

    posts = c.execute("SELECT * FROM post")
    return render_template('index.html', post=post, stamp=data, posts=posts)


if __name__ == "__main__":
    create_table()
    #data_entry()
    app.run()