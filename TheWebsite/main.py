from flask import Flask, request, url_for, session, render_template, redirect, flash
from functools import wraps
import time
import os
import sqlite3

import _login


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

#forgot_password is not in use as of now
@app.route("/forgot_password/", methods=['GET','POST'])
def forgot_password():

    #If user press Check button
    if request.method == "POST":
        attempted_username = request.form['username']
        attempted_email = request.form['email']

        global g_username
        g_username = attempted_username

        # Grab content from database
        username = c.execute("SELECT * FROM user WHERE username=(?)", (attempted_username,))
        username_data = username.fetchall()

        email = c.execute("SELECT * FROM user WHERE email=(?)", (attempted_email,))
        email_data = email.fetchall()

        if len(username_data) > 0 and len(email_data) > 0:
            #retrive password from database
            password = c.execute("SELECT password FROM user WHERE username=(?) AND email=(?)", (attempted_username, attempted_email, ))
            password_data = password.fetchall()

            flash("Password: " + str(password_data))
            #return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Try again.")
            # error = "Invalid credentials. Try again."

    return render_template('forgot_password.html')

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
    #flash(e)
    if request.method == "POST":
        attempted_username = request.form['username']
        attempted_email = request.form['email']

        attempted_password = request.form['password']
        attempted_confirm = request.form['confirm']

        # flash(attempted_username)
        # flash(attempted_password)

        x = c.execute("SELECT * FROM user WHERE username=(?)", (attempted_username, ))
        data = x.fetchall()

        if attempted_confirm != attempted_password:
            flash("The password does not match")
        elif attempted_username == "":
            flash("Username can not be empty")
        elif attempted_email == "":
            flash("Email can not be empty")
        elif attempted_password == "":
            flash("Password can not be empty")
        elif len(data) > 0:
            flash("There is already an account with that username")
        else:
            try:
                flash("Account created succesfully")
                c.execute("INSERT INTO user (username, email, password) VALUES(?,?,?)", (attempted_username, attempted_email, attempted_password))
                conn.commit()
                return redirect(url_for('login'))
            except:
                flash("Something went wrong")
                return redirect(url_for('register'))

            #flash(attempted_username)
            #flash(attempted_email)

            #flash(attempted_password)
            #flash(attempted_confirm)

    return render_template('register.html')

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
    #create_table()
    #data_entry()
    app.run()