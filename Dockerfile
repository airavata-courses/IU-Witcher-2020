FROM rabbitmq:3.7-management-alpine
#RUN apt-get update
#RUN apt-get install -y curl
EXPOSE 5672 32672 15671 15672
