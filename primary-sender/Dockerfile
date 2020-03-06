FROM debian:latest

RUN apt-get update && apt-get install -y \
    python3-pip

WORKDIR /primary-sender

COPY . /primary-sender

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5001

CMD [ "python3" , "primary_sender.py" ]
