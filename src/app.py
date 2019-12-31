__author__ = 'Hunter Files'

from flask import Flask, render_template, request, session, redirect, url_for

from src.common.database import Database
from src.models.user import User


app = Flask(__name__)    # '__main__'
app.secret_key = 'geralt'           # Witcher


@app.route('/')             # www.mysite.com/api
def home():
    return render_template('login.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/login', methods=['POST'])
def login():
    # after inserting the info in this function, when starting app.py it says
    # MODULENOTFOUND from src.models.user
    # what is happening?
    if request.method == 'POST':
        email = request.form.get("email")                  # request.form['id_of_element']
        password = request.form.get("password")

        if User.login_valid(email, password):
            User.login(email)
            # return redirect(url_for('home'))

    return render_template('profile.html', email=session['email'])


if __name__ == '__main__':
    app.run(port=4995, debug=True)
