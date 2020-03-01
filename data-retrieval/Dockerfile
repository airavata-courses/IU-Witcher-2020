<<<<<<< HEAD
FROM debian:latest

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get update && apt-get install -y \
    python3-pip

WORKDIR /data-retrieval

COPY . /data-retrieval

ENTRYPOINT ["tail", "-f", "/dev/null"]

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5003

CMD python3 -f data_retrieval.py
=======
FROM python:3.6

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

RUN python setup.py build_ext --inplace

EXPOSE 5001

ENTRYPOINT ["python"]
CMD ["data_retrieval.py"]
>>>>>>> 00abc3df922bc8b31a7452b8764df22dbfc4fbf4
