from src.common.database import Database

__author__ = 'Hunter Files'

# TODO finish User class
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
            return True
        else:
            # User exists :(
            # TODO add functionality to show on website that it failed
            return False

    def login(self):
        pass

    def get_blogs(self):
        pass

    def save_to_mongo(self):
        pass