import imageio
import rasterio
import numpy as np


def convert_jp2_to_jpeg(file_path_jp2, file_path_jpeg):
    pixels = read_image_pixels(file_path_jp2)
    save_image_pixels(pixels, file_path_jpeg)
    return file_path_jpeg


def read_image_pixels(file_path):
    with rasterio.open(file_path, "r+") as src:
        image_pixels = src.read()
    return image_pixels


def save_image_pixels(pixels, file_path):
    pixels_reshaped = pixels.squeeze()
    pixels_normalized = (
        (pixels_reshaped - pixels_reshaped.min())
        / (pixels_reshaped.max() - pixels_reshaped.min())
        * 255
    )
    pixels_uint8 = pixels_normalized.astype(np.uint8)
    imageio.imwrite(file_path, pixels_uint8.transpose(1, 2, 0))
