FROM debian:latest

RUN apt-get update && apt-get install -y \
    python3-pip

#FROM python:3.7

WORKDIR /data-retrieval

COPY . /data-retrieval

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5002

CMD [ "python3" , "data_retrieval.py" ]
