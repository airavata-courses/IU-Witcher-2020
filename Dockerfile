FROM rabbitmq:3.7-management-alpine
#RUN apt-get update
#RUN apt-get install -y curl
EXPOSE 6825 5671 5672 25672 15671 15672
