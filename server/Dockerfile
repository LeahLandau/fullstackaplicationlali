FROM jupyter/pyspark-notebook:python-3.11
WORKDIR /server
COPY . /server/
USER root
RUN pip install .
EXPOSE 5000
