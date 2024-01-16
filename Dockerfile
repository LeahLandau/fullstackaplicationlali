FROM node:16-alpine as build-step

ARG REACT_APP_SERVER_PATH
ENV REACT_APP_SERVER_PATH=$REACT_APP_SERVER_PATH

WORKDIR /app
COPY client/package.json client/package-lock.json ./
RUN npm install
COPY client .
RUN npm run build



FROM unit:1.31.1-python3.11
WORKDIR /app
COPY config.json /docker-entrypoint.d/config.json
COPY --from=build-step /app/build ./build
# COPY server/src/app.py /www/app.py
# COPY ./server ./server
COPY ./server ./www
WORKDIR /app/server
RUN pip install .
# WORKDIR /app/server/src

EXPOSE 8080

CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]