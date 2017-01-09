from flask import Flask, request, url_for, session, render_template, redirect, flash
from functools import wraps
import time
import os
import sqlite3


def register_required(cursor, conn):
    if request.method == "POST":
        attempted_username = request.form['username']
        attempted_email = request.form['email']

        attempted_password = request.form['password']
        attempted_confirm = request.form['confirm']

        # flash(attempted_username)
        # flash(attempted_password)

        x = cursor.execute("SELECT * FROM user WHERE username=(?)", (attempted_username, ))
        data = x.fetchall()


        #Check to see if user has filled in all fields
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
                cursor.execute("INSERT INTO user (username, email, password) VALUES(?,?,?)", (attempted_username, attempted_email, attempted_password))
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