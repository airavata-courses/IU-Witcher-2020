FROM ubuntu
#MAINTAINER Will Mayger
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential
RUN apt-get install -y python python-dev python-distribute python-pip
RUN git clone https://github.com/CanopyCloud/microservice-python
RUN pip install -r /microservice-python/requirements.txt
EXPOSE 5672
WORKDIR /message-broker
COPY . /message-broker
RUN rabbitmqctl add_user test testpass1
RUN rabbitmqctl add_vhost myvhost
RUN rabbitmqctl set_permissions -p myvhost test ".*" ".*" ".*"
RUN rabbitmq-server
