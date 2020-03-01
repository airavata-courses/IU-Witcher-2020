docker build -t srajpal/ads-data-retrieval:1.0 .

docker run -dit -td -p 5001:5001 srajpal/ads-data-retrieval:1.0 tail -f /dev/null
