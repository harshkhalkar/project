FROM mysql
ENV MYSQL_ROOT_PASSWORD=Pass1972
ENV MYSQL_DATABASE=info
COPY init.sql /docker-entrypoint-initdb.d
EXPOSE 3306
CMD ["mysqld"]
