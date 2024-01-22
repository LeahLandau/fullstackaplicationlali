FROM node:16-alpine as client-builder




ARG REACT_APP_SERVER_PATH
ENV REACT_APP_SERVER_PATH=$REACT_APP_SERVER_PATH

COPY client/package.json ./
RUN npm install
COPY client .
RUN npm run build


FROM unit:1.31.1-python3.11 as server-builder


COPY config.json /docker-entrypoint.d/config.json
COPY --from=client-builder /build ./build
COPY ./server ./www
WORKDIR /www
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org .
# RUN pip install .

EXPOSE 8080
