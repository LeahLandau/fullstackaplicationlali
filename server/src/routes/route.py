from flask import Blueprint, jsonify, request

from modules.files_paths import *
from modules.modify_image import *


routes = Blueprint('routes', __name__)

@routes.route('/api/blackening_pixels', methods=['POST'])
def blackening_pixels():
    try:
        print("11111111")
        body = request.get_json()
        result = modify_image(body['imagePath'], body['polygonFrame'])
        print("2222222222")
        if isinstance(result, str):
            return jsonify(result), 200
        return jsonify(result.args[0]), 200
    except Exception as error:
        print("33333333")
        return handle_error(error)

@routes.route('/api/get_images_names', methods=['GET'])
def get_images_and_folders_names():
    try:
        args = request.args
        if(args.get('directory_path') is None):
            return jsonify('The directory path must be provided'), 400
        result = get_images_names(args.get('directory_path'))
        print('result',result)
        if isinstance(result, FileNotFoundError):
            return result.args[0], 200
        return result, 200
    except Exception as error:
        return handle_error(error)

@routes.route('/images', methods=['POST'])
def images():
    return "Dfghdredgfghfggvhfgdresfdgd"