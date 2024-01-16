import unittest
from unittest.mock import patch, Mock

from routes.route import *
from app import *
from modules.modify_image import *


class TestBlackeningPixels(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    @patch('modules.files_paths.exists',Mock(return_value = True))
    @patch('modules.files_paths.splitext',Mock(return_value = ('image','.jp2')))
    @patch('modules.modify_image.full_polygon')
    @patch('modules.modify_image.open_read_write_image')
    def test_success(self, exists, splitext):
        response = self.app.post('/api/blackening_pixels', json={"imagePath": "image.jp2", "polygonFrame": "[[0,0]]"})
        self.assertEqual(response.status_code, 200)

    def test_invalid_endpoint(self):
        response = self.app.get('/api/invalid_endpoint')
        self.assertEqual(response.status_code, 404)

    def test_route_failed(self):
        response = self.app.post('/api/blackening_pixels', json={"imagePath": "image.png", "polygonFrame": "[[0,0]]"})
        self.assertEqual(response.status_code, 500)

class TestGetImagesAndFoldersNames(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    def test_bad_request(self):
        response = self.app.get('/api/get_images_names')
        self.assertEqual(response.status_code, 400)

    def test_invalid_endpoint(self):
        response = self.app.get('/api/invalid_endpoint')
        self.assertEqual(response.status_code, 404)
