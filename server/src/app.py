from flask import Flask

from routes.route import *
from waitress import serve

app = Flask(__name__,static_folder='/static', static_url_path='/')
app.register_blueprint(routes)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route('/api')
def api():
    return 'Image-Reduction'


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)