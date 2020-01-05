import datetime
import uuid

from src.common.database import Database
from src.models.post import Post

__author__ = 'Hunter'


class Blog(object):
    # MongoDB gives an ID called _id to each element
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    # uses the format from json and inserts it into database as data
    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    # dynamically changes to whatever class the method is created in. If we change the name from 'Blog' to 'Object',
    # it uses 'Object'
    @classmethod
    def from_mongo(cls, _id):
        # blog.from_mongo(blog_id) not "id"
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': _id})

        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]
