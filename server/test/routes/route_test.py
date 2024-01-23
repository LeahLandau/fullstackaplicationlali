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
    @patch('routes.route.handle_error', Mock(return_value="The path image.jp2 was not found") )
    def test_404(self):
        response=self.app.post('/api/blackening_pixels', json={"imagePath": "image.jp2", "polygonFrame": "[[0,0]]"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'<!doctype html>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The path image.jp2 was not found</p>\n')

    @patch('routes.route.modify_image', Mock(side_effect=Exception('Exception')) ) 
    @patch('routes.route.handle_error', Mock(return_value='Exception') )
    def test_400(self):
        response=self.app.post('/api/blackening_pixels', json={"imagePath": "image.jp2", "polygonFrame": "blablabla"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>Exception</p>\n')

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
    @patch('routes.route.handle_error', Mock(return_value="The path /not_exist_folder was not found") )
    def test_404(self):
        response=self.app.get('/api/get_images_names?directory_path=/not_exist_folder')
        self.assertEqual(response.data, b'<!doctype html>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The path /not_exist_folder was not found</p>\n' )
        self.assertEqual(response.status_code, 404)

    @patch('routes.route.get_images_names', Mock(side_effect=Exception("stat: path should be string, bytes, os.PathLike or integer, not NoneTyped")))
    @patch('routes.route.handle_error', Mock(return_value="stat: path should be string, bytes, os.PathLike or integer, not NoneType") )
    def test_400(self):
        response=self.app.get('/api/get_images_names')
        print(response.data)
        self.assertEqual(response.data, b'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>stat: path should be string, bytes, os.PathLike or integer, not NoneType</p>\n' )
        self.assertEqual(response.status_code, 400)

class TestConvertJP2toJPEG(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    @patch('routes.route.convert_jp2_to_jpeg', Mock(return_value='/images/jpeg/convert.jpeg'))
    def test_200(self):
        response = self.app.post('/api/convert_jp2_to_jpeg', json={
            "file_path_jp2": "image.jp2",
            "file_path_jpeg": "/images/jpeg/convert.jpeg"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'/images/jpeg/convert.jpeg')
        
    @patch('routes.route.convert_jp2_to_jpeg', Mock(side_effect=FileNotFoundError("The file image.jp2 was not found")))
    @patch('routes.route.handle_error', Mock(return_value="The file image.jp2 was not found"))
    def test_404(self):
        response = self.app.post('/api/convert_jp2_to_jpeg', json={
            "file_path_jp2": "image.jp2",
            "file_path_jpeg": "/images/jpeg/convert.jpeg"
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'<!doctype html>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The file image.jp2 was not found</p>\n')

        
    @patch('routes.route.convert_jp2_to_jpeg', Mock(side_effect=Exception('Exception')))
    @patch('routes.route.handle_error', Mock(return_value='Exception'))
    def test_400(self):
        response = self.app.post('/api/convert_jp2_to_jpeg', json={
            "file_path_jp2": "image.jp2",
            "file_path_jpeg": "/images/jpeg/convert.jpeg"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>Exception</p>\n')