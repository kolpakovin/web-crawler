import pymongo

class Database:
    URI = 'mongodb://127.0.0.1:27017'
    Database = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['firmwaredb']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def update(collection, query, data):
        return Database.DATABASE[collection].update_one({'_id': query}, data)

    @staticmethod
    def count_documents(collection, data):
        return Database.DATABASE[collection].count_documents(data)


Database.initialize()