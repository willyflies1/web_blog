__author__ = 'Hunter Files'

"""
    * Database class
"""
import pymongo


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    database = None

    @staticmethod  # means, we are not using self in this method
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.database = client['fullstack']             # changed from 'posts'

    @staticmethod
    def insert(collection, data):
        return Database.database[collection].insert(data)

    @staticmethod
    def find(collection, query):
        # Database.find('users', {'username': 'jose'})
        return Database.database[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.database[collection].find_one(query)
