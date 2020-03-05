docker build -t final_recv_id .

docker run --name final_recv -p 5011:5011 final_recv_id

#docker run -dit -t --name final-receiver -p 5011:5011 srajpal/ads-final-receiver:1.0 tail -f /dev/null
