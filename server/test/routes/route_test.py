import unittest
from unittest.mock import patch, Mock

from routes.route import *
from app import *
from modules.modify_image import *


class TestBlackeningPixels(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    def test_success(self):
        response = self.app.post('/api/blackening_pixels', json={"imagePath": "image.png", "polygonFrame": "[[0,0]]"})
        self.assertEqual(response.data, b'"The path image.png was not found"\n')
        self.assertEqual(response.status_code, 200)

    def test_invalid_endpoint(self):
        response = self.app.get('/api/invalid_endpoint')
        self.assertEqual(response.status_code, 404)

class TestGetImagesAndFoldersNames(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    def test_success(self):
        response = self.app.get('/api/get_images_names?directory_path=/server')
        self.assertEqual(response.status_code, 200)

    def test_bad_request(self):
        response = self.app.get('/api/get_images_names')
        self.assertEqual(response.status_code, 400)

    def test_invalid_endpoint(self):
        response = self.app.get('/api/invalid_endpoint')
        self.assertEqual(response.status_code, 404)

# class TestGetUrlByPath(unittest.TestCase):

#     def setUp(self):
#         self.app = app.test_client()

#     def test_get_url_by_path_route_without_path(self):
#         response = self.app.get('/api/get_url_by_path')
#         self.assertEqual(response.status_code, 400)    
#         self.assertEqual(response.data.decode(),'"The path must be provided"\n')

#     @patch('modules.files_paths.getUrlFromAzure',Mock(side_effect=Exception("The file /share/vistorage/path_not_exist was not found")))
#     def test_get_url_by_path_route_with_path_not_exist(self):
#         response = self.app.get('/api/get_url_by_path?path=temp/path_not_exist')
#         self.assertEqual(response.status_code, 200) 

#     @patch('modules.files_paths.getUrlFromAzure',Mock(return_value="url_with_sas"))
#     def test_get_url_by_path_route(self):
#         response = self.app.get('/api/get_url_by_path?path=temp/example1.png')
#         self.assertEqual(response.status_code, 200)