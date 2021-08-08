from flask import Flask, render_template, request
app = Flask(__name__)
# @app.route('/', methods=["GET", "POST"])
# def hello_world():
#     return render_template("index.html")

# app.route('/<queryString>', methods=['GET','POST'])

# def hello_world(query_string):
#     getData = request.args.get("method2")
#     postData = request.form.get("method3")
#     cookie = request.cookies.get("method4")
#     headers = request.headers.get("method5")
#     return {
#         "getData": getData,
#         "postData": postData,
#         "cookie": cookie,
#         "queryString": query_string
#     }



    
app.run(host="localhost", port=5000)