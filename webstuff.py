from flask import Flask, render_template, redirect, url_for, request, session
from functools import wraps
import server, threading, os


app = Flask(__name__)
app.secret_key = "Poggers"
app.template_folder = "./webs"
app.config['UPLOAD_FOLDER'] = os.getcwd()+"\\prints"
man = threading.Thread(target=server.main, name="server")
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    print(request.form)
    if request.method == 'POST':
        if request.form['username'] != 'hunter' or request.form['password'] != 'password':
            error = "Bad Creds"
        else:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html.jinja', error=error)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html.jinja', clients=server.CLIENTS, printers=server.PRINTERS, aviable=server.AVIABLE)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/printer/<id>', methods=['POST','GET'])
@login_required
def printer(id):
    if request.method == "POST":
        #print(request.files)
        if request.form.get("stop") is not None:
            server.CLIENTS[int(id)].send("stop")
        elif request.form.get("resume") is not None:
            server.CLIENTS[int(id)].send("resume")
        elif request.form.get("pause") is not None:
            server.CLIENTS[int(id)].send("pause")
        elif request.form.get("file") is not None:
            server.CLIENTS[int(id)].send("startPrint "+request.form.get("file"))

        if "file" in request.files:
            print("File being uploaded")
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                print("tranfering this file: ",app.config['UPLOAD_FOLDER']+"\\"+file.filename)
                print(server.CLIENTS[int(id)].fileTransfer(app.config['UPLOAD_FOLDER']+"\\"+file.filename))
        return redirect("/printer/{0}".format(id))
    return render_template('printer.html.jinja', printer=server.CLIENTS[int(id)])

# @app.route('/printer')
# def printe2r():
#     return render_template('printer.html.jinja', printer=id)


if __name__ == '__main__':
    #print("restarted")
    man.start()
    app.run()
    