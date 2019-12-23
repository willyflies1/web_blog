from datetime import datetime

from src.common.database import Database
from flask import Flask, session

__author__ = 'Hunter Files'

# TODO finish User class
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(collection='users',
                          query={'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection='users',
                          query={'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(self, email, password):
        # User.login_valid("hunter.files.me", password)
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user.password == password
    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exist, so we can create a new user
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists :(
            # TODO add functionality to show on website that it failed
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    # format for users stored in database
    def json(self):
        return {
            'email': self.email,
            '_id': self._id,
            'password': self.password       # not encrypted and not safe over network
        }

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(self, blog_id, title, content, date=datetime.datetime.utcnow()):
        # blog_id, title, content, author, created_date=datetime.datetime.utcnow()
        # find out what blog it is
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)


    def save_to_mongo(self):
        Database.insert('users', self.json())
