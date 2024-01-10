# from flask import Flask
# from flask_cors import CORS
# from waitress import serve

# # from routes.route import *
# app = Flask(__name__, static_folder='../build', static_url_path='/')
# # app = Flask(__name__)
# CORS(app) 
# # app.register_blueprint(routes)

# # print('fdsjkghkljghdlgkjshgkdfgdgdsgdfgdsgdfgsdgsdg')
# @app.route("/")
# def index():  

#     return app.send_static_file("index.html")

# if __name__ == '__main__':
#     serve(app, host="0.0.0.0", port=5000)
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
import json
# import numpy as np

sys.path.append('src') 
# from module import *

# app = Flask(__name__)
app = Flask(__name__, static_folder='../build', static_url_path='/')


CORS(app) 


@app.route("/")
def index():
    # return "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff" 
    return app.send_static_file("index.html")


@app.route("/hello_world")
def index1():
    return app.send_static_file("index.html")

@app.route('/blackening_pixels', methods=['POST'])
def blackening_pixels():
    body = request.get_json()
    result = modify_image(body['imagePath'], np.array(body.get('polygonFrame')))
    if type(result) != str:
        return jsonify(result.args[0])
    return jsonify(result)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
    
    
    
# from flask import Flask
# from flask_cors import CORS
# from waitress import serve

# from routes.route import *


# app = Flask(__name__)
# CORS(app) 
# app.register_blueprint(routes)

# @app.route('/api')
# def index():
#     return 'Image-Reduction'

# if __name__ == '__main__':
#     serve(app, host="0.0.0.0", port=5000)