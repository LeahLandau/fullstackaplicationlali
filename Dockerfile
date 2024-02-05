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

RUN pip install .

# RUN groupadd -g 1000 unitgroup && useradd -u 1000 -g unitgroup unituser

# USER root
# RUN mkdir -p /var/lib/unit/certs /var/lib/unit/scripts /var/run/unit /var/log/unit \
#     && chown -R unituser:unitgroup /var/lib/unit /var/log/unit \
#     && chmod -R 775 /var/lib/unit /var/log/unit \
#     && mkdir -p /var/run/unit \
#     && chown unituser:unitgroup /var/run/unit \
#     && chmod 775 /var/run/unit

# USER unituser:unitgroup
RUN chown -R unit:unit /app/
RUN chown -R unit:unit /static/
RUN chown -R unit:unit /var/
# RUN chmod-socket=666
RUN chmod 666 /docker-entrypoint.d/config.json

USER unit:unit

EXPOSE 8080


# CMD ["unitd", "--no-daemon", "--control", "0.0.0.0:8080"]
