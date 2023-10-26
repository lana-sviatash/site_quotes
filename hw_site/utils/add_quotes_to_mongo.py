import json
from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient("mongodb://localhost")

db = client.hw_site

with open("quotes.json", "r", encoding="utf-8") as fd:
    quotes = json.load(fd)

for quote in quotes:
    for author_name in quote['author']:
        author = db.authors.find_one({'fullname': author_name})
        if author:
            db.quotes.insert_one({
                "quote": quote["quote"],
                "tags": quote["tags"],
                "author": ObjectId(author["_id"]),
            })
