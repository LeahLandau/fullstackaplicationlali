import unittest
from unittest.mock import patch, Mock

from routes.route import *
from app import *


class TestBlackeningPixels(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    @patch('routes.route.modify_image', Mock(return_value='The image has been blackened successfully'))
    def test_200(self):
        response=self.app.post('/api/blackening_pixels', json={"imagePath": "image.jp2", "polygonFrame": "[[0,0]]"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'The image has been blackened successfully')

    @patch('routes.route.modify_image', Mock(side_effect=FileNotFoundError("The path image.jp2 was not found")) ) 
    def test_404(self):
        response=self.app.post('/api/blackening_pixels', json={"imagePath": "image.jp2", "polygonFrame": "[[0,0]]"})
        self.assertEqual(response.status_code, 404)

    @patch('routes.route.modify_image', Mock(side_effect=Exception('Exception')) ) 
    def test_400(self):
        response=self.app.post('/api/blackening_pixels', json={"imagePath": "image.jp2", "polygonFrame": "blablabla"})
        self.assertEqual(response.status_code, 400)

class TestGetImagesNames(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    @patch('routes.route.get_images_names', Mock(return_value=[]))
    def test_200(self):
        response=self.app.get('/api/get_images_names?directory_path=/images')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'[]\n' )
    
    @patch('routes.route.get_images_names', Mock(side_effect=FileNotFoundError("The path /not_exist_folder was not found")))
    def test_404(self):
        response=self.app.get('/api/get_images_names?directory_path=/not_exist_folder')
        self.assertEqual(response.status_code, 404)

    @patch('routes.route.get_images_names', Mock(side_effect=Exception("stat: path should be string, bytes, os.PathLike or integer, not NoneTyped")))
    def test_400(self):
        response=self.app.get('/api/get_images_names')
        print(response.data)
        self.assertEqual(response.status_code, 400)