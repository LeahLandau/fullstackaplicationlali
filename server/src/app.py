from flask import Flask

from routes.route import *


app = Flask(__name__,static_folder='/static', static_url_path='/')
app.register_blueprint(routes)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route('/api')
def api():
    return 'Image-Reduction'

@app.route('/app')
def tryv():
    return app.static_folder