import rasterio
from os.path import exists,splitext
import numpy as np
from shapely.geometry import Polygon,Point

from .handle_error import *
from .files_paths import *

def modify_image(file_path, polygon_frame):
  try:
    path_exist(file_path) 
    file_is_jp2_image(file_path) 
    polygon_pixels = full_polygon(polygon_frame)
    open_read_write_image(file_path, polygon_pixels)
  except Exception as error:
    return handle_error(error)
  return 'The image has been blackened successfully'
  
def file_is_jp2_image(file_path):
  if not splitext(file_path)[1] =='.jp2':
    raise Exception('The file is not a jp2 image')

def full_polygon(polygon_frame):
  try:
    polygon_fill = fill_polygon(polygon_frame)
    return np.concatenate((polygon_frame, polygon_fill), axis = 0)
  except Exception as error:
    raise Exception(error)
    
def fill_polygon(polygon_frame):
  try:
    minx, miny = np.min(polygon_frame, axis=0)
    maxx, maxy = np.max(polygon_frame, axis=0)
    return np.array([[x, y] for x in range(int(minx)+1, int(maxx)) for y in range(int(miny)+1, int(maxy)) if Polygon(polygon_frame).contains(Point(x, y))])
  except:
    raise Exception('Invalid polygon frame')

def open_read_write_image(file_path, matrix_of_pixels):
  try: 
    with rasterio.open(file_path, 'r+') as src:
      image_pixels = src.read()
      image_pixels = blackening_pixels(image_pixels, matrix_of_pixels) 
      src.write(image_pixels)
      src.close()
  except:
    raise Exception('The matrix is not valid')

def blackening_pixels(image_pixels, matrix_of_pixels):
  try:
    for pixel in matrix_of_pixels:
      row, column = pixel
      image_pixels[:, row, column] = 0
  except:
      raise Exception('The matrix is not valid')
  return image_pixels