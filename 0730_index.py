from flask import Flask, render_template, send_file, request, make_response
app = Flask(__name__)
# @app.route('/', methods=["GET", "POST"])
# def hello_world():
#     return render_template("index.html")

@app.route('/<query_string>', methods=['GET','POST'])

def hello_world(query_string):
    if request.method == 'GET':
        return render_template('form.html')
    getData = request.args.get("method2")
    postData = request.form.get("method3")
    cookie = request.cookies.get("method4")
    headers = request.headers.get("method5")
    res = make_response({
        "getData": getData,
        "postData": postData,
        "cookie": cookie,
        "header": headers,
        "queryString": query_string
    })
    res.set_cookie('method4', 'vnit-cookie')
    return res

app.run(host="localhost", port=5000)