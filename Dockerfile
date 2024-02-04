FROM node:16-alpine as client-builder

ARG REACT_APP_IMAGES_VOLUME_NAME=/images
ENV REACT_APP_IMAGES_VOLUME_NAME=${REACT_APP_IMAGES_VOLUME_NAME}

COPY client/package.json ./
RUN npm install
COPY client .
RUN npm run build


FROM unit:1.31.1-python3.11 as server-builder


ARG SERVER_IMAGES_VOLUME_NAME=/static
ENV SERVER_IMAGES_VOLUME_NAME=${SERVER_IMAGES_VOLUME_NAME}

ARG ERROR_HANDLER=/var/log/errors.log
ENV ERROR_HANDLER=${ERROR_HANDLER}

COPY config.json /docker-entrypoint.d/config.json
COPY --from=client-builder /build ./static
COPY ./server ./app
WORKDIR /app
# RUN pip install .
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org .
# RUN chown -R unit:unit /path/to/venv/
# RUN chown -R unit:unit 
RUN chmod -R 777 .
USER unit

EXPOSE 8080

