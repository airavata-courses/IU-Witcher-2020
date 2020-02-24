FROM alpine:3.7

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app/model-execution

COPY . /app/model-execution

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5002

CMD ["python3", "model_execution.py"]



