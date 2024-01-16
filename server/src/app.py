from flask import Flask
from flask_cors import CORS
from waitress import serve

# from routes.route import *


app = Flask(__name__,static_folder='../../build', static_url_path='/')
CORS(app) 
app.register_blueprint(routes)

@app.route("/")
def index():
    return app.send_static_file("index.html")

# @app.route('/api')
# def index():
#     return 'Image-Reduction'

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
