#Build Image

docker-compose up -d

#For assigning on network

docker network connect --alias phpserver mynetwork [containerId]

