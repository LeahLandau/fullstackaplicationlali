import os
from os.path import exists, splitext
from azure.storage.file import FileService
from datetime import datetime, timedelta
from dotenv import load_dotenv

from .handle_error import *

load_dotenv()

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

def get_url_from_azure(file_path):
  try:
    path_exist(f"/share/vistorage/{file_path}")
    file_service = FileService(account_name=os.environ.get('USER'), account_key=os.environ.get('PASSWORD'))
    sas_token = file_service.generate_file_shared_access_signature(
        os.environ.get('SHARE_NAME'),
        None,
        file_path,
        permission='r',
        expiry=datetime.now() + timedelta(hours=24),
    )
  except Exception as error:
    return handle_error(error)
  sas_url = f"https:{os.environ.get('DEVICE')}/{file_path}?{sas_token}"
  return sas_url