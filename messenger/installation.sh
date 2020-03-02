docker pull rabbitmq:3-management

docker run -d -p 8004:15672 -p 8003:5672 --name rabbitmq-server rabbitmq:3-management
