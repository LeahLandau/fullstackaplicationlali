from flask import Blueprint, jsonify, request, abort

from modules.files_paths import *
from modules.modify_image import *
from modules.handle_error import *


routes = Blueprint('routes', __name__)

@routes.route('/api/blackening_pixels', methods=['POST'])
def blackening_pixels():
    try:
        body = request.get_json()
        result = modify_image(body['imagePath'], body['polygonFrame'])
        return result, 200
    except FileNotFoundError as error:
        error = handle_error(error)
        abort(404, error)
    except Exception as error:
        error = handle_error(error)
        abort(400, error)

@routes.route('/api/get_images_names', methods=['GET'])
def get_images_and_folders_names():
    try:
        args = request.args
        if(args.get('directory_path') is None):
            return jsonify('The directory path must be provided'), 400
        result = get_images_names(args.get('directory_path'))
        if isinstance(result, FileNotFoundError):
            return result.args[0], 200
        return result, 200
    except Exception as error:
        return handle_error(error)

@routes.route('/api/get_url_by_path', methods=['GET'])
def get_url_by_path():
    try:
        args = request.args    
        if(args.get('path') is None):
            return jsonify('The path must be provided'),400
        result = get_url_from_azure(args.get('path'))
        if isinstance(result, str):
            return jsonify(result),200
        return jsonify(result.args[0]) ,200
    except Exception as error:
        return handle_error(error)