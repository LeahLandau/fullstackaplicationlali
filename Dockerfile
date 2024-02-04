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

# Ensure the required directories have proper permissions
USER root
RUN chown -R unit:unit /var/lib/unit /var/run/unit /var/log/unit
USER unit:unit

RUN pip install .

USER unit:unit

EXPOSE 8080
