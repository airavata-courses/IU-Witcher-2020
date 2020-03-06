docker build -t model_exec_id .

docker run --name model_exec -p 5002:5002 model_exec_id
