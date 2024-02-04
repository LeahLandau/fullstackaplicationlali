# FROM node:16-alpine as client-builder

# ARG REACT_APP_IMAGES_VOLUME_NAME=/images
# ENV REACT_APP_IMAGES_VOLUME_NAME=${REACT_APP_IMAGES_VOLUME_NAME}

# COPY client/package.json ./
# RUN npm install
# COPY client .
# RUN npm run build


# FROM unit:1.31.1-python3.11 as server-builder

# ARG SERVER_IMAGES_VOLUME_NAME=/static
# ENV SERVER_IMAGES_VOLUME_NAME=${SERVER_IMAGES_VOLUME_NAME}

# ARG ERROR_HANDLER=/var/log/errors.log
# ENV ERROR_HANDLER=${ERROR_HANDLER}

# COPY config.json /docker-entrypoint.d/config.json
# COPY --from=client-builder /build ./static
# COPY ./server ./app
# WORKDIR /app


# RUN pip install .

# USER root
# RUN if [ ! -d "/var/lib/unit/certs" ]; then mkdir -p /var/lib/unit/certs; fi \
#     && if [ ! -d "/var/lib/unit/scripts" ]; then mkdir -p /var/lib/unit/scripts; fi \
#     && chown -R unit:unit /var/lib/unit

# USER unit:unit

# EXPOSE 8080

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

RUN adduser -D unituser

RUN mkdir -p /var/lib/unit/certs /var/lib/unit/scripts \
    && chown -R unituser:unituser /var/lib/unit

USER unituser

RUN pip install .

USER unituser

EXPOSE 8080

