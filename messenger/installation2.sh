docker build -t srajpal/ads-messenger:1.0 .

docker run -it -d -p 5007:5007 srajpal/ads-messenger:1.0 /bin/sh
