docker build -t akshaygpt/ads-ui:1.0 .
docker run -it -d -p 3000:3000 akshaygpt/ads-ui:1.0 /bin/sh
