import setuptools

setuptools.setup(
    name="image-reduction",
    version="1.0.0",
    package_dir = { 
        "": "src" 
    },
    install_requires = [
        "rasterio",
        "gunicorn",
        "numpy",
        "pytest",
        "pytest_mock",
        "flask",
        "flask-cors",
        "waitress",
        "shapely",
        "pyspark",
        "azure-storage-file",
        "python-dotenv",
    ],
    extras_require ={
        "tests": ["pytest", "pytest_mock"],
        "server":["flask", "flask-cors", "waitress"],
        "geographic_processing":["rasterio", "shapely",  "numpy"],
        "spark":["pyspark"],
        "Azure_communication":[ "azure-storage-file", "python-dotenv" ],
    },
)