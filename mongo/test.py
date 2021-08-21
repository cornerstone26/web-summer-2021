from pymongo import MongoClient
import random


mongo = MongoClient('localhost', 27017)
db = mongo.wad
print(db.users.find({}))

for user in db.users.find({}):
    print(user)

username = random.randint(0,10)
password = random.randint(0,100)
db.users.insert_one({
    "username": username,
    "password": password
})