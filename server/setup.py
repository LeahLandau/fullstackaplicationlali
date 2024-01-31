import setuptools

setuptools.setup(
    name="image-reduction",
    version="1.0.0",
    package_dir={"": "src"},
    install_requires=[
        "rasterio",
        "numpy",
        "imageio",
        "pytest",
        "pytest_mock",
        "flask",
        "flask-cors",
        "waitress",
        "shapely",
    ],
    extras_require={
        "tests": ["pytest", "pytest_mock"],
        "server": ["flask", "flask-cors", "waitress"],
        "geographic_processing": ["rasterio", "shapely", "numpy", "imageio"],
    },
)
