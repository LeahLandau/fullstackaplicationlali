import os
from os.path import exists, splitext

from .handle_error import *

def path_exist(file_path):
  if not exists(file_path):
    raise FileNotFoundError(f'The path {file_path} was not found')

def image_in_required_format(image_name, image_format):
    return splitext(image_name)[1] == image_format

def get_images_names(directory_path):
        path_exist(directory_path)
        image_names = []
        for dirpath, dirnames, files in os.walk(directory_path):
            image_names += append_jp2_images(dirpath, files)
        return image_names

def append_jp2_images(dirpath, files):
        jp2_image_names = []
        for file_name in files:
            if image_in_required_format(file_name, '.jp2'):
                jp2_image_names.append(os.path.join(dirpath, file_name) )
        return jp2_image_names