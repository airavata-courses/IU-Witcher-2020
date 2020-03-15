docker build -t prim_send_id .

docker run --name prim_send -p 5010:5010 prim_send_id
