FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org gunicorn


EXPOSE 5000


CMD ["gunicorn", "app:app", "--config=config/gunicorn_config.py"]
