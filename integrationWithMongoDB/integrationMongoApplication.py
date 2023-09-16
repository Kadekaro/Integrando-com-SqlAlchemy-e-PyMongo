import datetime
import pprint

import pymongo as pym

client = pym.MongoClient("mongodb+srv://kadekaro:<password>@clusterteste.zjv7moo.mongodb.net/?retryWrites=true&w"
                         "=majority")
db = client.test
collection = db.test_collection
print(f"\n{db.test_collection}")

# Definição de informação para definir o documento:
post = {
    "autor": "Wesley",
    "text": "My first MongoDB applicated based on python",
    "tags": ["mongodb", "python3", "pymongo"],
    "date": datetime.datetime.utcnow()
}

# preparando para submeter as informações:
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(f"\n{post_id}\n")

# print(db.posts.find_one())
pprint.pprint(db.posts.find_one())

# bulk inserts:
new_posts = [{
    "author": "Nelsa",
    "text": "Another post",
    "tags": ["bulk", "post", "insert"],
    "date":datetime.datetime.utcnow()
    },
    {
    "author": "Márcia",
    "text": "Post from Márcia. New post available",
    "title": "MongoDB Atlas is Fun",
    "date": datetime.datetime(2009, 11, 10, 10, 45)
    }]

result = posts.insert_many(new_posts)
print(f'\nRecuperando os ids:\n{result.inserted_ids}\n')

print("\nRecuperando informações:")
pprint.pprint(db.posts.find_one({"author": "Márcia"}))

print("\nRecuperando muitas informações de uma vez:")
for post in posts.find():
    pprint.pprint(post)
