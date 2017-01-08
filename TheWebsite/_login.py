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