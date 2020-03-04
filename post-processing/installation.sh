docker build -t srajpal/ads-post-processing:1.0 .

docker run -it -d --name post_proc -p 5003:5003 srajpal/ads-post-processing:1.0 /bin/sh
