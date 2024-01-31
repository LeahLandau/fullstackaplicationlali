FROM node:16-alpine as client-builder

ARG REACT_APP_IMAGES_VOLUME_NAME
ENV REACT_APP_IMAGES_VOLUME_NAME=$REACT_APP_IMAGES_VOLUME_NAME

ARG REACT_APP_SERVER_PATH
ENV REACT_APP_SERVER_PATH=$REACT_APP_SERVER_PATH

COPY client/package.json ./
RUN npm install
COPY client .
RUN npm run build


FROM unit:1.31.1-python3.11 as server-builder

ARG SERVER_IMAGES_VOLUME_NAME
ENV SERVER_IMAGES_VOLUME_NAME=$SERVER_IMAGES_VOLUME_NAME

# USER root
COPY config.json /docker-entrypoint.d/config.json
COPY --from=client-builder /build ./static
COPY ./server ./app
WORKDIR /app
# RUN pip install .
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org .


# RUN useradd -m -s /bin/bash newspace
# USER newspace
EXPOSE 8080

# FROM node:16-alpine as client-builder

# ARG REACT_APP_SERVER_PATH
# ENV REACT_APP_SERVER_PATH=$REACT_APP_SERVER_PATH

# COPY client/package.json ./
# RUN npm install
# COPY client .
# RUN npm run build


# FROM unit:1.31.1-python3.11 as server-builder

# COPY config.json /docker-entrypoint.d/config.json
# COPY --from=client-builder /build ./static
# COPY ./server ./app
# WORKDIR /app
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org .
# EXPOSE 8080


# FROM node:16-alpine as client-builder

# ARG REACT_APP_SERVER_PATH
# ENV REACT_APP_SERVER_PATH=$REACT_APP_SERVER_PATH

# COPY client/package.json ./
# RUN npm install
# COPY client .
# RUN npm run build


# FROM unit:1.31.1-python3.11 as server-builder

# COPY config.json /docker-entrypoint.d/config.json
# COPY --from=client-builder /build ./static
# COPY ./server ./app
# WORKDIR /app
# RUN pip install .

# EXPOSE 8080
