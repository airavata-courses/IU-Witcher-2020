docker build -t data_retrv_id .

docker run --name data_retrv -p 5001:5001 data_retrv_id
