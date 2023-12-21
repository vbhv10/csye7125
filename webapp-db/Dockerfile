FROM flyway/flyway:9

# Copy your Flyway configuration file (e.g., flyway.conf) into the image
COPY flyway.conf /flyway/conf/

# Copy your SQL migration scripts into the image
COPY ./migrations/* /flyway/sql

ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_SCHEMA=${DB_SCHEMA}
