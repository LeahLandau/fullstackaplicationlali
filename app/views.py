from app import app

@app.route('/')
def hello():
    return "Hello, Flask on Azure Container App!"
