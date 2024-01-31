import unittest
from unittest.mock import patch, Mock
import numpy as np

from modules.modify_image import (
    modify_image,
    full_polygon,
    fill_polygon,
    open_read_write_image,
    blackening_pixels,
    file_is_jp2_image,
)


class TestModifyImage(unittest.TestCase):
    @patch("modules.files_paths.exists", Mock(return_value=True))
    @patch("modules.files_paths.splitext", Mock(return_value=("input/cake", ".jp2")))
    @patch("modules.modify_image.full_polygon")
    @patch("modules.modify_image.open_read_write_image")
    def test_success_blackening_an_image(self, exists, splitext):
        result = modify_image(
            "input/cake.jp2",
            np.array(
                [
                    [5, 1],
                    [6, 1],
                    [7, 2],
                    [8, 2],
                    [9, 1],
                    [9, 2],
                    [9, 3],
                    [8, 4],
                    [7, 5],
                    [6, 4],
                    [6, 3],
                    [5, 3],
                    [4, 2],
                ]
            ),
        )
        self.assertEqual(result, "The image has been blackened successfully")

    @patch("modules.files_paths.exists", Mock(return_value=False))
    def test_file_path_doesnt_exist(self):
        with self.assertRaises(Exception) as context:
            modify_image(
                "blablabla",
                np.array(
                    [
                        [5, 1],
                        [6, 1],
                        [7, 2],
                        [8, 2],
                        [9, 1],
                        [9, 2],
                        [9, 3],
                        [8, 4],
                        [7, 5],
                        [6, 4],
                        [6, 3],
                        [5, 3],
                        [4, 2],
                    ]
                ),
            )
        self.assertEqual(str(context.exception), "The path blablabla was not found")

    @patch("modules.files_paths.exists", Mock(return_value=True))
    @patch("modules.files_paths.splitext", Mock(return_value=("input/cake", ".jpg")))
    def test_file_is_not_jp2_image(self):
        with self.assertRaises(Exception) as context:
            modify_image(
                "input/cake.jpg",
                np.array(
                    [
                        [5, 1],
                        [6, 1],
                        [7, 2],
                        [8, 2],
                        [9, 1],
                        [9, 2],
                        [9, 3],
                        [8, 4],
                        [7, 5],
                        [6, 4],
                        [6, 3],
                        [5, 3],
                        [4, 2],
                    ]
                ),
            )
        self.assertEqual(str(context.exception), "The file is not a jp2 image")

    @patch("modules.files_paths.exists", Mock(return_value=True))
    @patch("modules.files_paths.splitext", Mock(return_value=("input/cake", ".jp2")))
    @patch(
        "modules.modify_image.full_polygon",
        Mock(side_effect=ValueError("Invalid polygon frame")),
    )
    def test_polygon_frame_is_invalid(self):
        with self.assertRaises(Exception) as context:
            modify_image("input/cake.jp2", "blablabla")
        self.assertEqual(str(context.exception), "Invalid polygon frame")


class TestFileIsJp2Image(unittest.TestCase):
    @patch("modules.files_paths.splitext", Mock(return_value=("input/cake", ".jp2")))
    def test_file_is_jp2_image(self):
        result = file_is_jp2_image("input/cake.jp2")
        self.assertEqual(result, None)

    def test_file_is_not_jp2_image(self):
        with self.assertRaises(Exception) as context:
            file_is_jp2_image("input/cake.jpg")
        self.assertEqual(str(context.exception), "The file is not a jp2 image")


class TestFullPolygon(unittest.TestCase):
    @patch(
        "modules.modify_image.fill_polygon",
        Mock(return_value=np.array([[5, 2], [6, 2], [7, 3], [8, 3], [7, 4]])),
    )
    def test_polygon_frame_is_valid(self):
        result = full_polygon(
            "[[5,1] ,[6,1], [7,2], [8,2] ,[9,1], [9,2] ,[9,3], [8,4], [7,5], [6,4], [6,3], [5,3] ,[4,2]]"
        )
        np.testing.assert_almost_equal(
            result,
            np.array(
                [
                    [5, 1],
                    [6, 1],
                    [7, 2],
                    [8, 2],
                    [9, 1],
                    [9, 2],
                    [9, 3],
                    [8, 4],
                    [7, 5],
                    [6, 4],
                    [6, 3],
                    [5, 3],
                    [4, 2],
                    [5, 2],
                    [6, 2],
                    [7, 3],
                    [8, 3],
                    [7, 4],
                ]
            ),
        )

    @patch(
        "modules.modify_image.fill_polygon",
        Mock(side_effect=ValueError("Invalid polygon frame")),
    )
    def test_polygon_frame_is_invalid(self):
        with self.assertRaises(Exception):
            full_polygon("blablabla")


class TestFillPolygon(unittest.TestCase):
    def test_polygon_frame_is_invalid(self):
        with self.assertRaises(Exception):
            fill_polygon("blablabla")

    def test_polygon_frame_is_valid(self):
        result = fill_polygon(
            [
                [5, 1],
                [6, 1],
                [7, 2],
                [8, 2],
                [9, 1],
                [9, 2],
                [9, 3],
                [8, 4],
                [7, 5],
                [6, 4],
                [6, 3],
                [5, 3],
                [4, 2],
            ]
        )
        np.testing.assert_almost_equal(
            result, np.array([[5, 2], [6, 2], [7, 3], [7, 4], [8, 3]])
        )


class TestOpenReadWriteImage(unittest.TestCase):
    @patch("modules.modify_image.rasterio.open")
    def test_the_matrix_is_valid(self, open):
        result = open_read_write_image("input/cake.jp2", np.array([[0, 0], [0, 1]]))
        self.assertEqual(result, None)

    def test_the_image_is_not_exist(self):
        with self.assertRaises(Exception) as context:
            open_read_write_image("input/cake.jp2", "blablabla")
        self.assertEqual(
            str(context.exception), "input/cake.jp2: No such file or directory"
        )


class TestBlackeningPixels(unittest.TestCase):
    def test_success_to_blackening_pixels(self):
        np.testing.assert_almost_equal(
            blackening_pixels(
                np.array([[[205, 120, 117]], [[14, 5, 136]], [[20, 11, 142]]]),
                np.array([[0, 0], [0, 0]]),
            ),
            np.array([[[0, 120, 117]], [[0, 5, 136]], [[0, 11, 142]]]),
        )

    def test_failed_to_blackening_pixels(self):
        with self.assertRaises(Exception) as context:
            blackening_pixels("blablabla", np.array([[0, 0], [0, 1]]))
        self.assertEqual(
            str(context.exception), "'str' object does not support item assignment"
        )
