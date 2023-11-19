# app.py
from flask import Flask, render_template, jsonify, request, redirect, flash, session, url_for 
from flask_pymongo import PyMongo
import subprocess
import os
from functools import wraps
import uuid

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user"

mongo = PyMongo(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "is_user_logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorised access", "warning")
            return redirect(url_for("login"))

    return decorated_function


@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print("its a post call")
        print(request.form["name"])
        name = request.form["name"]
        phnumber = request.form["phnumber"]

        mongo.db.users.insert_one(
            {
                "name": name,
                "phnumber": phnumber, 
                
            }
        )

        flash("User registered successfull", "success")

        return redirect(url_for('index'))

    print("its an get call")    
    
    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    # bussiness logic
    if request.method == "POST":
        # accept data from frontend(form data) - > email and password
        name = request.form["name"]
        phnumber = request.form["phnumber"]

        # Check if that email is present in database or not
        found_user = mongo.db.users.find_one({"phnumber": phnumber})
        # print(found_user)
        if found_user:
            print("user found")
            # # if email is present then compare password_hash from db with user's entered password
            # is_password_matched = bcrypt.check_password_hash(
            #     found_user["password"], password
            # )

            if found_user:
                print("correct password")
                # if password also matched then login successfull and redirect to dashboard
                session["is_user_logged_in"] = True
                session["name"] = found_user["name"]
                session["phnumber"] = found_user["phnumber"]
                
                flash("Login successfull", "success")
                return redirect("/index")
            else:
                print("incorrect password")
                flash("Invalid password provided", "danger")

        else:
            print("no user found")
            flash("User not registered", "danger")

    return render_template("login.html")



@app.route('/index/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/start-voice-assistant')
def start_voice_assistant():
    try:
        # Assuming voice_assistant.py is in the same directory
        script_path = os.path.join(os.path.dirname(__file__), 'voice_assistant.py')
        subprocess.Popen(['python', script_path])
        return jsonify({'status': 'success', 'message': 'Voice assistant started successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out", "success")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.secret_key = "shfgdekhh"
    print(app.url_map)
    app.run(debug=True)
