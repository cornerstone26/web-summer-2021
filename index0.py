from flask import Flask, request, render_template, make_response, redirect, flash
from flask_pymongo import PyMongo
import app_config
from model.user0 import User
from app import mongo, app
from functools import wraps

def login_required(func):
    @wraps(func)
    def login_func(*arg, **kwargs):
        try:
            obj = User.from_db(request.cookies.get('username'))
            print(obj.token, "login_func")
            if obj.authorize(request.cookies.get('token')):
                return func(*arg, **kwargs)
        except:
            pass
        flash("Login required!!!")
        return redirect('/login')
    
    return login_func

def no_login(func):
    @wraps(func)
    def no_login_func(*arg, **kwargs):
        try:
            username = request.cookies.get('username')
            if (mongo.db.users.find_one({"user": username}).authorize(request.cookies.get('token'))):
                flash("You're already in!")
                return redirect('/')
        except:
            pass
        return func(*arg, **kwargs)
    
    return no_login_func

@app.route('/')
def home():
    return redirect('/index')

@app.route('/index')
@login_required
def index():
    return render_template('0817_index.html', text="Welcome to WAD VNIT 2021!!!")

@app.route('/login', methods=['POST', 'GET'])
@no_login
def login():
    if request.method == 'GET':
        return render_template('0817_login.html')
    
    username, password = request.form.get('username'), request.form.get('password')
    
    if mongo.db.users.find_one({"user": username}) != None:
        obj = User.from_db(username)
        if obj.authenticate(password): 
            token = obj.init_session()
            resp = make_response(redirect('/index'))
            resp.set_cookie('username', username)
            resp.set_cookie('token', token)
            return resp
        else:
            flash("Username or password does not correct!!!")
    else: 
        flash ("User does not exist")

    return render_template('0817_login.html')
 
@app.route('/logout', methods = ['POST'])
@login_required
def logout():
    username = request.cookies.get('username')
    obj = User.from_db(username)
    obj.terminate_session()
    resp = make_response(redirect('/login'))
    resp.delete_cookie('username')
    resp.delete_cookie('token')
    flash("You've logged out")
    return resp

@app.route('/register', methods=['POST', 'GET'])
@no_login
def register():
    if request.method == "GET":
        return render_template('0817_register.html')
    
    username, password, password_confirm = request.form.get('username'), request.form.get('password'), request.form.get('password_confirm')
    obj = mongo.db.users.find_one({"user":username})
    if obj == None:
        if password == password_confirm:
            obj = User.new(username, password)
            token = obj.init_session()
            resp = make_response(redirect('/index'))
            resp.set_cookie('username', username)
            resp.set_cookie('token', token)
            return resp
        else:
            flash("Passwords don't match!")
    else:
        flash("Username already exists")
    
    return render_template('0817_register.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
