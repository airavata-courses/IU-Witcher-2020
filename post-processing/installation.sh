docker build -t post_proc_id .

docker run --name post_proc -p 5003:5003 post_proc_id
