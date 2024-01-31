from flask import Blueprint, request, abort, current_app

from modules.files_paths import *
from modules.modify_image import *
from modules.convert_jp2 import *
from modules.handle_error import *

routes = Blueprint('routes', __name__)

@routes.route('/api/blackening_pixels', methods=['POST'])
def blackening_pixels():
    try:
        body = request.get_json()
        # result = modify_image(current_app.static_folder + body['imagePath'], body['polygonFrame'])
        result = modify_image("/static" +body['imagePath'], body['polygonFrame'])
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
        directory_path = request.args.get('directory_path')
        # directory_path = current_app.static_folder + directory_path
        directory_path = "/static" + directory_path
        result = get_images_names(directory_path)
        return result, 200
    except FileNotFoundError as error:
        error = handle_error(error)
        abort(404, error)
    except Exception as error:
        error = handle_error(error)
        abort(400, error)
        
@routes.route('/api/convert_jp2_to_jpeg', methods=['POST'])
def convert_jp2():
    try:
        body = request.get_json()
        # result = convert_jp2_to_jpeg(current_app.static_folder + body['file_path_jp2'],current_app.static_folder + body['file_path_jpeg'] )
        result = convert_jp2_to_jpeg('/static'+body['file_path_jp2'],'/static'+body['file_path_jpeg'] )
        _, _, result = result.partition('/static')
        return result, 200
    except FileNotFoundError as error:
        error = handle_error(error)
        abort(404, error)
    except Exception as error:
        error = handle_error(error)
        abort(400, error)        