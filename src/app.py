__author__ = 'Hunter Files'

from flask import Flask, render_template, request, session, redirect, url_for

from src.common.database import Database
from src.models.blog import Blog
from src.models.user import User


app = Flask(__name__)    # '__main__'
app.secret_key = 'geralt'           # Witcher


@app.route('/')
def home_template():
    return render_template('login.html')


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
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if User.login_valid(email, password):
            User.login(email)
        else:
            session['email'] = None
            return render_template('login.html')        #, failed_login=True

    return render_template('profile.html', email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        User.register(email, password)

        return render_template('profile.html', email=session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_name=blog.title)


if __name__ == '__main__':
    app.run(port=4995, debug=True)
