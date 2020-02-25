docker build -t akshaygpt/ads-model-execution:1.0 .
docker run -it -d -p 5002:5002 akshaygpt/ads-model-execution:1.0 /bin/sh
