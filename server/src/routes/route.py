from flask import Blueprint, request, abort
import os

from modules.files_paths import get_images_names
from modules.modify_image import modify_image
from modules.handle_error import handle_error
from modules.convert_jp2 import convert_jp2_to_jpeg


routes = Blueprint("routes", __name__)


@routes.route("/api/blackening_pixels", methods=["POST"])
def blackening_pixels():
    try:
        volume_name = os.environ.get("SERVER_IMAGES_VOLUME_NAME", "/static")
        body = request.get_json()
        result = modify_image(volume_name + body["imagePath"], body["polygonFrame"])
        return result, 200
    except FileNotFoundError as error:
        error = handle_error(error)
        abort(404, error)
    except Exception as error:
        error = handle_error(error)
        abort(400, error)


@routes.route("/api/get_images_names", methods=["GET"])
def get_images_and_folders_names():
    try:
        volume_name = os.environ.get("SERVER_IMAGES_VOLUME_NAME", "/static")
        args = request.args
        result = get_images_names(volume_name + args.get("directory_path"))
        return [path.replace(volume_name, "") for path in result], 200
    except FileNotFoundError as error:
        error = handle_error(error)
        abort(404, error)
    except Exception as error:
        error = handle_error(error)
        abort(400, error)


@routes.route("/api/convert_jp2_to_jpeg", methods=["POST"])
def convert_jp2():
    try:
        volume_name = os.environ.get("SERVER_IMAGES_VOLUME_NAME", "/static")
        body = request.get_json()
        file_path_jp2 = volume_name + body["file_path_jp2"]
        file_path_jpeg = volume_name + body["file_path_jpeg"]
        result = convert_jp2_to_jpeg(file_path_jp2, file_path_jpeg)
        return result.replace(volume_name, ""), 200
    except FileNotFoundError as error:
        error = handle_error(error)
        abort(404, error)
    except Exception as error:
        error = handle_error(error)
        abort(400, error)
