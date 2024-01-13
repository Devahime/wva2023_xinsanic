from flask import Flask, render_template, request

from database import database

app = Flask(__name__, static_folder='static', static_url_path='/static')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

@app.route("/")
def index():
    #return '<a href="http://127.0.0.1:5000/html/index.html">Dovážková služba</a>'
    return render_template('/html/index.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)