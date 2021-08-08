from flask import Flask, render_template
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")

app.route('/<queryString>', methods=['POST'])
def index(queryString):
    
app.run(host="localhost", port=5000)