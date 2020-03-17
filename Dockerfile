FROM debian:latest

RUN apt-get update && apt-get install -y \
    python3-pip

#FROM python:3.7

WORKDIR /app/model-execution

COPY . /app/model-execution

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5003

CMD [ "python3" , "model_execution.py" ]
