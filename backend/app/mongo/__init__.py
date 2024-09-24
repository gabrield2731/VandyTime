from pymongo import MongoClient

client = MongoClient()

def init_mongo(app):
    client = MongoClient(app.config["MONGO_URI"])
    return client
 