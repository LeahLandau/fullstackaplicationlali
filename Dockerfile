# FROM nginx/unit:1.19.0-python3.7
FROM unit:1.31.1-python3.11

EXPOSE 8080

COPY requirements.txt /config/requirements.txt
RUN python3 -m pip install -r /config/requirements.txt
COPY config.json /docker-entrypoint.d/config.json
# COPY app.py /www/app.py