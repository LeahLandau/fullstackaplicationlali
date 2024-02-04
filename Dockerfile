# Stage 1: Build the client application
FROM node:16-alpine as client-builder

ARG REACT_APP_IMAGES_VOLUME_NAME=/images
ENV REACT_APP_IMAGES_VOLUME_NAME=${REACT_APP_IMAGES_VOLUME_NAME}

COPY client/package.json ./
RUN npm install
COPY client .
RUN npm run build

# Stage 2: Build the server application
FROM unit:1.31.1-python3.11 as server-builder

ARG SERVER_IMAGES_VOLUME_NAME=/static
ENV SERVER_IMAGES_VOLUME_NAME=${SERVER_IMAGES_VOLUME_NAME}

ARG ERROR_HANDLER=/var/log/errors.log
ENV ERROR_HANDLER=${ERROR_HANDLER}

COPY config.json /docker-entrypoint.d/config.json

# Copy static files from the client-builder stage
COPY --from=client-builder /build ./static
COPY ./server ./app



# Set the working directory
WORKDIR /app

# Install the server application
RUN pip install .

# Create a non-root user and group
RUN groupadd -g 1000 unitgroup && useradd -u 1000 -g unitgroup unituser

# Ensure the required directories have proper permissions
USER root
RUN mkdir -p /var/lib/unit/certs /var/lib/unit/scripts /var/run/unit /var/log/unit \
    && chown -R unituser:unitgroup /var/lib/unit /var/run/unit /var/log/unit \
    && chmod -R 775 /var/lib/unit /var/run/unit /var/log/unit

# Switch to the non-root user
USER unituser:unitgroup

# Command to run the application
# CMD ["unitd", "--no-daemon", "--control", "0.0.0.0:8080"]
