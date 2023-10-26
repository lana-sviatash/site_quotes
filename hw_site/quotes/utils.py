from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb://localhost")
    db = client.hw_site
    return db