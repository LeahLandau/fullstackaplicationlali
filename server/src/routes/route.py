import json
from flask import Blueprint, jsonify, request

from modules.files_paths import *
from modules.modify_image import *


routes = Blueprint('routes', __name__)

@routes.route('/api/blackening_pixels', methods=['POST'])
def blackening_pixels():
    body = request.get_json()
    result = modify_image(body['imagePath'], body['polygonFrame'])
    if isinstance(result, str):
        return jsonify(result), 200
    return jsonify(result.args[0]), 200

@routes.route('/api/get_images_names', methods=['GET'])
def get_images_and_folders_names():
    args = request.args
    if(args.get('directory_path') is None):
        return jsonify('The directory path must be provided'), 400
    result = get_images_names(args.get('directory_path'))
    if isinstance(result, FileNotFoundError):
        return result.args[0], 200
    return result, 200

@routes.route('/api/get_url_by_path', methods=['GET'])
def get_url_by_path():
    args = request.args    
    if(args.get('path') is None):
        return jsonify('The path must be provided'),400
    result = getUrlFromAzure(args.get('path'))
    if isinstance(result, str):
        return jsonify(result),200
    return jsonify(result.args[0]) ,200