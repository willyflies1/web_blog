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

        """     OLD...
        title = input("Enter post title: ")
        content = input("Enter post content: ")
        # TODO CHANGE DEFAULT VALUE FOR DATETIME
        date = input("Enter post date, or leave blank for today ( in format DDMMYYYY): ")
        if date == '':
            date=datetime.datetime.utcnow()
        else:
            date = datetime.datetime.strptime(date, "%d%m%Y")
        """
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.saveToMongo()

    def get_posts(self):
        return Post.fromBlog(self._id)

    # uses the format from json and inserts it into database as data
    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    # The format of the object we are using.
    def json(self):
        return {
            'id': self._id,
            'author_id': self.author_id,
            # 'blog_id': self.blog_id,
            'author': self.author,
            'title': self.title,
            'description': self.description,
        }

    # dynamically changes to whatever class the method is created in. If we change the name from 'Blog' to 'Object',
    # it uses 'Object'
    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]