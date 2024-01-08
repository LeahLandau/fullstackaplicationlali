import unittest
from unittest.mock import patch, Mock

from modules.files_paths import *
from modules.handle_error import *


class TestFileExist(unittest.TestCase):

    @patch('modules.files_paths.exists',Mock(return_value = False))
    def test_path_not_exist(self):
        with self.assertRaises(Exception) as context:
           path_exist('blablabla')
        self.assertEqual(str(context.exception), 'The path blablabla was not found')
 
    @patch('modules.files_paths.exists',Mock(return_value = True))
    def test_path_exist(self):
        result = path_exist('/images')
        self.assertEqual(result, None)

class TestImageInRequiredFormat(unittest.TestCase):

    def test_image_not_in_required_format(self):     
        result = image_in_required_format('image.jpg', '.jp2')
        self.assertFalse(result)

    def test_image_in_required_format(self):                                                                                                                                             
        result = image_in_required_format('image.jpeg', '.jpeg')
        self.assertTrue(result)

class TestGetImagesNames(unittest.TestCase):

    @patch('modules.files_paths.exists', Mock(return_value=False))
    def test_path_not_exist(self):
        result = get_images_names('blablabla')
        self.assertEqual(result.args[0], 'The path blablabla was not found')

    @patch('modules.files_paths.exists', Mock(return_value=True))
    @patch('modules.files_paths.os.walk', Mock(return_value=[('/server/check', [], ['b.jp2']), ('/server/check/a', [], ['d.jp2'])]))
    def test_path_exist(self):
        result = get_images_names('/server/check')
        self.assertEqual(result, ['/server/check/b.jp2', '/server/check/a/d.jp2'])

class TestAppendJp2Images(unittest.TestCase):

    def test_one_of_the_inputs_is_invalid(self):
        with self.assertRaises(Exception) as context:
           append_jp2_images('/server', 2121)
        self.assertEqual(str(context.exception), 'One of the received data is invalid')

    def test_the_inputs_is_valid(self):
        result = append_jp2_images('/server', [])
        self.assertEqual(result, [])