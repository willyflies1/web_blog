__author__ = 'Hunter Files'

from flask import Flask, render_template, request, session, redirect, url_for

from src.common.database import Database
from src.models.user import User


app = Flask(__name__)    # '__main__'
app.secret_key = 'geralt'           # Witcher

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login')             # LOCALHOST:4993/login
def login_template():
    return render_template('login.html')

@app.route('/register')             # www.mysite.com/api
def register_template():
    return render_template('register.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/auth/login', methods=['POST'])
def login():
    # after inserting the info in this function, when starting app.py it says
    # MODULENOTFOUND from src.models.user
    # what is happening?
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if User.login_valid(email, password):
            User.login(email)
        else:
            session['email'] = None

    return render_template('profile.html', email=session['email'])

@app.route('/auth/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        User.register(email, password)
        # session['email'] = email, DONE INSIDE User.py/register()

        return render_template('profile.html', email=session['email'])


if __name__ == '__main__':
    app.run(port=4995, debug=True)
