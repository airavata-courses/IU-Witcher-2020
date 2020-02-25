FROM alpine:3.7

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app/post-processing

COPY . /app/post-processing

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5003

CMD ["python3", "post_processing.py"]
