# from flask import Flask
# from flask_cors import CORS
# from waitress import serve

# from routes.route import *


# app = Flask(__name__)
# CORS(app) 
# # app.register_blueprint(routes)
# @app.route('/')
# def index():
#     return "welcome, client"

# @app.route('/api')
# def index():
#     return "welcome server running"

# if __name__ == '__main__':
#     serve(app, host="0.0.0.0", port=8080)

from flask import Flask
app = Flask(__name__)
# application = app


@app.route('/')
def hello_world():
    return 'Hello, World!'
