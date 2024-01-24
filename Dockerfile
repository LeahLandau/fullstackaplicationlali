FROM node:16-alpine as client-builder

ARG REACT_APP_SERVER_PATH
ENV REACT_APP_SERVER_PATH=$REACT_APP_SERVER_PATH

COPY client/package.json ./
RUN npm install
COPY client .
RUN npm run build


FROM unit:1.31.1-python3.11 as server-builder

COPY config.json /docker-entrypoint.d/config.json
COPY --from=client-builder /build /app/static
COPY ./server /app
WORKDIR /app
RUN pip install .

EXPOSE 8080
