from flask import Flask, render_template, request, Response
import time
import threading
app = Flask(__name__)
cnt = 0

def inc():
    global cnt
    while True:
        time.sleep(1)
        cnt += 1

#XMLHttpRequest
@app.route('/')
def home():
    return render_template('_index.html')

@app.route('/add', methods=['POST'])
def addition():
    a = request.form.get('a')
    b = request.form.get('b')

    result = int(a) + int(b)
    
    return str(result)

#Short polling
@app.route('/short', methods=['GET', 'POST'])
def short_handler():
    global cnt
    if request.method == 'GET':
        return render_template('_short.html')
    else:
        cnt += 1
        if cnt % 2 == 0:
            return str(cnt)
        else:
            return Response('', status=500)

#Long polling
@app.route('/long', methods=['GET', 'POST'])
def long_handler():
    global cnt
    if request.method == 'GET':
        thread = threading.Thread(target=inc)
        thread.start()
        return render_template('_long.html')
    elif request.method == 'POST':
        return str(cnt)
    else:
        return Response('', status=405)

if __name__ == '__main__':
    app.run()