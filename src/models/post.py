"""
    Post to database server.
"""
__author__ = 'Hunter'

import uuid
import datetime
from src.common.database import Database


"""
    Class: Post
    Param: {int} blog_id, {String} title, {String} content, {datetime} function, {int} id=None
    Descr: Posts a blog to the database server. 
           Currently running MongoDB 4.2.1
"""


class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self.id = uuid.uuid4().hex if _id is None else _id  # should "self.id" be "self._id"

    # post = Post(blog_id="123", title="a title", content="some content", author="Hunter", datetime.datetime.utcnow())
    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        # creates a json representation of the post itself
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        # return Database.find(collection='posts', query={'blog_id': id})
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
