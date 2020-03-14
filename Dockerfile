#FROM debian:latest

#RUN apt-get update && apt-get install -y \
#    python3-pip

FROM python:3.7

WORKDIR /post_processing

COPY . /post_processing

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5004

CMD [ "python3" , "post_processing.py" ]
