__author__ = 'Hunter Files'

from flask import Flask, render_template

app = Flask(__name__)    # '__main__'


@app.route('/') # www.mysite.com/api/
def hello_method():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=4995)
