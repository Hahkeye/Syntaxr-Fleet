from flask import Flask, render_template, redirect, url_for, request, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "Poggers"

def login_required(x):
    @wraps(x)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return x(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/home')
def home():
    return 'Nothing'

@app.route('/login',methods = ['GET','POST'])
def login():
    error = ""
    if request.method == 'POST':
        if request.form['username'] != 'hunter' or request.form['password'] != 'password':
            error = "Bad Creds"
        else:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
    

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))