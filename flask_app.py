from chatbot import chatbot
from flask import Flask, flash, render_template, request, jsonify, send_file, session,  make_response, url_for, redirect
from flask_cors import CORS, cross_origin
import dashboard
import json
import jwt
from functools import wraps
from datetime import timedelta, datetime
import jwt
from config import systemConfig

dashboard_obj = dashboard.Dashboard()


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.static_folder = 'static'
app.secret_key = systemConfig.flask_secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1440)


@app.after_request
def after_request(response):
    response.headers.set("Access-Control-Allow-Credentials", "true")
    return response


def token_check(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        form_data = request.get_json(force=True)
        status = dashboard_obj.auth_request(form_data)
        if status == 'success':
            form_data.pop("jwt_token")
            return func(form_data, *args, **kwargs)
        return {"status": status, "response": [], "message": "Authentication Error"}

    return decorated


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))


@app.route("/dashboard/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form_data = {
            "username": request.form['username'], "password": request.form['password']}
        data = dashboard_obj.auth_user(form_data)
        if data["status"] == 'success':
            try:
                payload = {
                    'exp': datetime.utcnow() + timedelta(days=0, hours=12),
                    'iat': datetime.utcnow(),
                    'username': form_data['username'],
                    'password': form_data['password']
                }
                token = jwt.encode(
                    payload,
                    systemConfig.jwt_secret_key,
                    algorithm='HS256'
                )
                gen_token = token.decode('UTF-8')
            except:
                flash("Error! JWT token Exception", "danger")
                return redirect(url_for('login'))
            session["username"] = form_data["username"]
            session["jwt_token"] = gen_token

            flash("Login successful", "success")
            return redirect(url_for('dash_add'))
        flash(data["message"], "danger")
        return redirect(url_for('login'))

    return render_template("login.html")


@app.route('/dashboard/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        form_data = {
            "username": request.form['username'], "password": request.form['password']}
        data = dashboard_obj.register_user(form_data)

        if data["status"] == 'success':
            flash("User Registration Successful", "success")
            return redirect(url_for('login'))

        flash(data["message"], "danger")
        return redirect(url_for('register'))

    return render_template('register.html')


@app.route("/dashboard/add")
def dash_add():
    if 'username' in session:
        return render_template("add.html")
    else:
        flash("Please Login", "warning")
        return redirect(url_for('login'))


@app.route("/dashboard/delete")
def dash_delete():
    if 'username' in session:
        return render_template("delete.html")
    else:
        flash("Please Login", "warning")
        return redirect(url_for('login'))


@app.route("/dashboard/show")
def dash_show():
    if 'username' in session:
        return render_template("show.html")
    else:
        flash("Please Login", "warning")
        return redirect(url_for('login'))


@app.route("/dashboard/logout")
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('jwt_token')
        flash("Logout successful", "success")
    return redirect(url_for('login'))


@app.route('/dashboard/delete_query', methods=['POST'])
@token_check
def delete_query(status, form_data):
    output_json = {}

    data = dashboard_obj.delete_query(form_data)

    output_json = {
        "status":   data['status'],
        "response": data['response'],
        "message":  data['message']
    }
    return jsonify(output_json)


@app.route('/dashboard/add_query', methods=['POST'])
@token_check
def add_query(status, form_data):
    output_json = {}

    data = dashboard_obj.add_query(form_data)

    output_json = {
        "status":   data['status'],
        "response": data['response'],
        "message":  data['message']
    }
    return jsonify(output_json)


@app.route('/dashboard/list_query', methods=['POST'])
@token_check
def list_query(status, form_data):
    output_json = {}

    data = dashboard_obj.list_query()

    output_json = {
        "status":   data['status'],
        "response": data['response'],
        "message":  data['message']
    }
    return jsonify(output_json)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
