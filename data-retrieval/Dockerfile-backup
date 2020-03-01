FROM alpine:3.7

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app/data-retrieval

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5001

CMD ["python3", "data_retrieval.py"]



