import werkzeug.exceptions
from flask import Flask, url_for, request, render_template, redirect, make_response, session, escape, jsonify, Response, \
    abort
from werkzeug.utils import secure_filename
import os
import json
from functools import wraps

# from OpenSSL import SSL

# context = SSL.Context(SSL.TLSv1_2_METHOD)
# context.use_certificate("mycert.crt")
# context.use_privatekey("myprivatekey.key")

app = Flask(__name__)
folder = "/home/karali/PycharmProjects/Flask_1/"
extensions = set(["txt", "jpg", "png"])


def check(username, password):
    return username == "admin" and password == "180122de"


def auth():
    return Response('Please login!', 401, {'WWW-Authenticate': 'Basic real = "Login Required'})


def requires_auth(f):
    @wraps(f)
    def deco(*args, **kwargs):
        autho = request.authorization
        if not autho or not check(autho.username, autho.password):
            return auth()
        return f(*args, **kwargs)

    return deco


@app.route('/adminpanel')
@requires_auth
def adminpanel():
    return "Hello Admin"


@app.route("/path/", defaults={'path': ''})
@app.route("/<path:path>")
def path(path):
    return "Hello Word" + path


@app.errorhandler(werkzeug.exceptions.NotFound)
def notFound(e):
    return jsonify(error=str(e), mykey=42, list=[42, 112]), e.code


def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions


@app.route("/postme/", methods=['GET'])
def postMe():
    postedjson = json.loads(request.data.decode('utf-8'))
    print(postedjson)
    return "Success"


@app.route("/sessions_logout")
def logout():
    session.pop('name', None)
    return redirect(url_for('sessions'))


@app.route("/sessions_login", methods=["GET", "POST"])
def sessions():
    print(os.urandom(24))
    if request.method == "POST":
        session['name'] = request.form['name']
        return redirect(request.url)
    else:
        if 'name' in session:
            return "Hello" + escape(session['name'])
        else:
            return render_template("session.html")


app.secret_key = "b'\xaa/f\x9dgA\x04\xd4\xf77\x82\xa3\x7f\x0f\xbcG\xe4\x987\x94\x19\x81]H'"


@app.route("/date_update", methods=["GET", "POST"])
def dateUpdate():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == "":
            return redirect(request.url)
        if allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))
            return redirect(request.url)
    return render_template("data.html")


# @app.route("/")
# def index():
#     return "Welcome to title page!"


@app.route("/a_href")
def index2():
    return '<a href=' + url_for("hello_Int", name=1) + '> HelloWord'


@app.route("/")
def index():
    # abort(404)
    app.logger.info("Main Route")
    return render_template('index.html', fantasie="Flask Tutorials", param=50)


@app.route("/login", methods=['POST', 'GET'])
def login():
    name = ""
    cookie = request.cookies.get('username')
    if cookie is not None:
        return "Hello " + cookie
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.get('name')
    resp = make_response("Hello" + name + "!")
    resp.set_cookie('username', name)
    return resp


@app.route("/hello")
def hello():
    return "Hello World!"


@app.route("/hello/<string:name>")
def hello_String(name):
    return "Hello " + name + "!"


@app.route("/hello/int/<int:name>")
def hello_Int(name):
    return "Hello " + str(name + 2) + "!"


@app.route("/hello/float/<float:name>")
def hello_Float(name):
    return "Hello " + str(name + 2.0) + "!"


@app.route("/hello/path/<path:name>")
def hello_Path(name):
    return "Hello " + name + "!"


if __name__ == '__main__':
    app.run(debug=True, port=1802)
