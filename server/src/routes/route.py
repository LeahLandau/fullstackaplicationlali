from flask import Blueprint, jsonify, request, abort

from modules.files_paths import *
from modules.modify_image import *


routes = Blueprint('routes', __name__)

@routes.route('/api/blackening_pixels', methods=['POST'])
def blackening_pixels():
    try:
        body = request.get_json()
        result = modify_image(body['imagePath'], body['polygonFrame'])
        return result, 200
    except FileNotFoundError as error:
        abort(404, str(error))
    except Exception as error:
        abort(400, str(error))

@routes.route('/api/get_images_names', methods=['GET'])
def get_images_and_folders_names():
    try:
        args = request.args
        result = get_images_names(args.get('directory_path'))
        return result, 200
    except FileNotFoundError as error:
        abort(404, str(error))
    except Exception as error:
        abort(400, str(error))