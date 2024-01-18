import rasterio
import numpy as np
from shapely.geometry import Polygon,Point

from .handle_error import *
from .files_paths import *

def modify_image(file_path, polygon_frame):
    print("4444444444444")
    file_path = f'/build/{file_path}'
    print(file_path)
    path_exist(file_path) 
    print("ddddddddddddddd")
    # file_is_jp2_image(file_path) 
    polygon_pixels = full_polygon(polygon_frame)
    open_read_write_image(file_path, polygon_pixels)
    return 'The image has been blackened successfully'
  
def file_is_jp2_image(file_path):
  if not image_in_required_format(file_path, '.jp2'):
    raise Exception('The file is not a jp2 image')

def full_polygon(polygon_frame):
    polygon_frame = json.loads(polygon_frame)
    polygon_fill = fill_polygon(polygon_frame)
    if polygon_fill.size == 0:
      return polygon_frame
    return np.concatenate((polygon_frame, polygon_fill), axis = 0)
    
def fill_polygon(polygon_frame):
    minx, miny = np.min(polygon_frame, axis=0)
    maxx, maxy = np.max(polygon_frame, axis=0)
    return np.array([[x, y] for x in range(int(minx)+1, int(maxx)) for y in range(int(miny)+1, int(maxy)) if Polygon(polygon_frame).contains(Point(x, y))])

def open_read_write_image(file_path, matrix_of_pixels):
    with rasterio.open(file_path, 'r+') as src:
      image_pixels = src.read()
      image_pixels = blackening_pixels(image_pixels, matrix_of_pixels) 
      src.write(image_pixels)
      src.close()

def blackening_pixels(image_pixels, matrix_of_pixels):
    for pixel in matrix_of_pixels:
      row, column = pixel
      image_pixels[:, row, column] = 0
    return image_pixels
  