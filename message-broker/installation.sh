docker pull rabbitmq:3-management

#docker run --name mess_rabbit -p 127.0.0.1::15672 rabbitmq:3-management

docker run --name mess_rabbit -p 8004:15672 -p 8003:5672 rabbitmq:3-management

#docker run -d --name mess_rabbit -p 8004:15672 -p 8003:5672 --name rabbitmq-server rabbitmq:3-management
