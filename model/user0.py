import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
import app_config
from app import mongo, app

def gen_session_token(length=24):
    token = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)]) 
    return token

class User:
    def __init__(self, username, password, token='None'):
        self.username = username
        # self.password = generate_password_hash(password)
        self.password = password
        self.token = token
        self.dump(1)

    @classmethod
    def new(cls,username, password):
        password = generate_password_hash(password)
        return cls(username, password)
    
    @classmethod
    def from_db(cls, user):
        username = mongo.db.users.find_one({"user": user})['user']
        password = mongo.db.users.find_one({"user": user})['password'] 
        token = mongo.db.users.find_one({"user": user})['token']
        if token == 'None':
            return cls(username, password)
        return cls(username, password, token) 
    
    def authenticate(self, password):
        return check_password_hash(self.password, password)
        # return password == self.password
    
    def init_session(self):
        self.token = gen_session_token()
        self.dump(2)
        return self.token
    
    def authorize(self, token):
        return token == self.token

    def terminate_session(self):
        self.token = 'None'
        self.dump(3)

    # def __str__(self):
    #     return f'{self.username};{self.password};{self.token}'

    def dump(self, index):
        mongo.db.users.update_one({"user": self.username},{'$set': {"user": self.username, "password": self.password, "token":self.token}},upsert=True)
        print(self.token, index)