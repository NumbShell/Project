from flask import Flask, request, url_for, session, render_template, redirect, flash
from functools import wraps


# login_required method is coded by Sentdex.
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


"""
class FormTemplate():

    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""
        self.error = ""

    def verify_user(self, cursor, username, password):
        try:
            if request.method == "POST":
                #Set username and password
                self.username = username
                self.password = password

                flash(self.username)
                flash(self.password)

                # Grab content from database
                username = cursor.execute("SELECT * FROM user WHERE username=(?)", (self.username,))
                username_data = username.fetchall()

                password = cursor.execute("SELECT * FROM user WHERE password=(?)", (self.password,))
                password_data = password.fetchall()

                #if user exist then log in and set sessions
                if len(username_data) > 0 and len(password_data) > 0:
                    # user = attempted_username
                    session['logged_in'] = True
                    session['username'] = self.username

                    flash("You are now logged in")
                    return redirect(url_for('home'))
                else:
                    flash("Invalid credentials. Try again.")
                    # error = "Invalid credentials. Try again."

            return render_template("login.html", error=self.error)

        except Exception as e:
            return render_template('login.html', error=self.error)

        return render_template('login.html')
"""



"""def verify_users(self, cursor):
        if request.method == "POST":
            # Grab user from database
            username = cursor.execute("SELECT * FROM user WHERE username=(?)", (self.username,))
            username_data = username.fetchall()

            email = cursor.execute("SELECT * FROM user WHERE email=(?)", (self.email,))
            email_data = email.fetchall()

            #If username exist in db then ...
            if len(username_data) > 0 and len(email_data) > 0:
                # retrive password from database
                password = cursor.execute("SELECT password FROM user WHERE username=(?) AND email=(?)",
                                 (self.username, self.email,))
                password_data = password.fetchall()

                flash("Password: " + str(password_data))
                # return redirect(url_for('home'))
            else:
                flash("Invalid credentials. Try again.")
                # error = "Invalid credentials. Try again."
"""



"""
class LoginRequest(FormTemplate):




class RegisterRequest(FormTemplate):
"""

