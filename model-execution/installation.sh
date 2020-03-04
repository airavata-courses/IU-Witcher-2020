docker build -t srajpal/ads-model-execution:1.0 .

docker run -it -d --name model_exec -p 5002:5002 srajpal/ads-model-execution:1.0 /bin/sh
