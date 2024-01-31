import unittest
from unittest.mock import patch, Mock, MagicMock
import numpy as np

from modules.convert_jp2 import (
    convert_jp2_to_jpeg,
    read_image_pixels,
    save_image_pixels,
)
from modules.modify_image import file_is_jp2_image


class TestConvertJp2ToJpeg(unittest.TestCase):
    @patch("modules.convert_jp2.read_image_pixels")
    @patch("modules.convert_jp2.save_image_pixels")
    def test_success_convert(self, exists, splitext):
        result = convert_jp2_to_jpeg("a.jp2", "convert.jpeg")
        self.assertEqual(result, "convert.jpeg")

    @patch("modules.convert_jp2.read_image_pixels", return_value=MagicMock())
    @patch("modules.convert_jp2.save_image_pixels")
    def test_convert_failure(cls, mock_save_image_pixels, mock_read_image_pixels):
        with cls.assertRaises(Exception) as context:
            file_is_jp2_image("input/cake.jpg")
        cls.assertEqual(str(context.exception), "The file is not a jp2 image")


class TestReadImagePixels(unittest.TestCase):
    @patch("modules.convert_jp2.rasterio.open")
    def test_read_image_pixels_success(self, mock_rasterio_open):
        mock_src = Mock()
        mock_src.read.return_value = "mocked_pixels"
        mock_rasterio_open.return_value.__enter__.return_value = mock_src
        file_path = "/path/to/image.jp2"
        result = read_image_pixels(file_path)
        mock_rasterio_open.assert_called_once_with(file_path, "r+")
        mock_src.read.assert_called_once()
        self.assertEqual(result, "mocked_pixels")

    @patch(
        "modules.convert_jp2.rasterio.open", side_effect=Exception("Mocked exception")
    )
    def test_read_image_pixels_failure(self, mock_rasterio_open):
        file_path = "/path/to/image.jp2"
        with self.assertRaises(Exception) as context:
            read_image_pixels(file_path)
        mock_rasterio_open.assert_called_once_with(file_path, "r+")
        self.assertEqual(str(context.exception), "Mocked exception")


class TestSaveImagePixels(unittest.TestCase):
    @patch("imageio.imwrite")
    def test_save_image_pixels_success(self, mock_imwrite):
        pixels = np.random.randint(0, 256, (3, 100, 100), dtype=np.uint8)
        file_path = "output/image.jpg"
        save_image_pixels(pixels, file_path)
        self.assertTrue(
            np.array_equal(mock_imwrite.call_args[0][1], pixels.transpose((1, 2, 0)))
        )

    @patch("imageio.imwrite", side_effect=Exception("Failed to save image"))
    def test_save_image_pixels_failure(self, mock_imwrite):
        pixels = np.random.randint(0, 256, (3, 100, 100), dtype=np.uint8)
        file_path = "output/image.jpg"
        with self.assertRaises(Exception) as context:
            save_image_pixels(pixels, file_path)
        self.assertEqual(str(context.exception), "Failed to save image")
