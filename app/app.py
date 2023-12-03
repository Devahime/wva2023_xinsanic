from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return '<a href="http://127.0.0.1:5000/index">Dovážková služba</a>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)