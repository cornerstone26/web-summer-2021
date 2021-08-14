from flask import Flask, render_template, request, redirect, make_response
from functools import wraps
app = Flask(__name__)

def generate_token(user,pwd):
    return user + ':' + pwd

@app.route('/')
def home():
    return redirect('/login'), 301

def auth(request):
    token = request.cookies.get('login-info')
    try:
        user, pwd = token.split(':')
    except:
        return False
    if (user == 'admin' and pwd == 'admin'):
        return True
    else:
        return False
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = request.form.get('user')
        pwd = request.form.get('password')

        if user == 'admin' and pwd == 'admin':
            token = generate_token(user, pwd)
            resp = make_response(redirect('/index'))
            resp.set_cookie('login-info', token)
            return resp
        else:
            return redirect('/login'), 403

def auth_required(f):
    @wraps(f)
    def check(*arg, **kwargs):
        if (auth(request)):
            return f(*arg, **kwargs)
        else:
            return redirect('/')
    return check

@app.route('/index') 
# def index(): #Cach nay lau
#     token = request.cookies.get('login-info')
#     try:
#         user, pwd = token.split(':')
#     except:
#         return redirect('/')
#     if (user == 'admin' and pwd == 'admin'):
#         return render_template('0813index.html')
#     else:
#         return redirect('/')

# def index(): 
#     if auth(request):
#         return render_template('0813index.html')
#     else:
#         return redirect('/')

#Cach nay dung decorator
@auth_required
def index():
    return render_template('0813index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)