FROM python:3.11
WORKDIR /app
COPY . /app/
USER root
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org .
# RUN pip install .
RUN useradd -m -s /bin/bash newspace
USER newspace
EXPOSE 5000