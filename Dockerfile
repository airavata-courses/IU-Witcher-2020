FROM php:7.1.2-apache 
COPY . /var/www/html
RUN chmod 777 auth.txt