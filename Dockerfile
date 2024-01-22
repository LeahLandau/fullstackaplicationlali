FROM node:16-alpine as client-builder

# --- NETFREE CERT INTSALL ---
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
RUN cat  /home/netfree-unix-ca.sh | sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
# --- END NETFREE CERT INTSALL ---


ARG REACT_APP_SERVER_PATH
ENV REACT_APP_SERVER_PATH=$REACT_APP_SERVER_PATH

# COPY client/package.json client/package-lock.json ./
# RUN npm install -g npm@10.3.0
# RUN npm install
# COPY client .
# RUN npm run build


# FROM unit:1.31.1-python3.11 as server-builder


# COPY config.json /docker-entrypoint.d/config.json
# COPY --from=client-builder /build ./build
# COPY ./server ./www
# WORKDIR /www

# RUN pip install .

# EXPOSE 8080
