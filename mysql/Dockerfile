FROM mysql:latest
ENV MYSQL_DATABASE=appWithAPIdb \
    MYSQL_ROOT_PASSWORD=some_secret
ADD ./initdb.sql /docker-entrypoint-initdb.d/
