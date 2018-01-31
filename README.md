# Dockerfiles
Put all the useful Dockerfiles into this repo

## How to build docker image with docker file

If you have created corresponding repo in the docker hub, you can directly use:

```
Take EDB-34164 as example,

cd EDB-34164;
docker build -t mudongliang/edb-34164 .

docker run -i -t mudongliang/edb-34164 /bin/bash

# change something

docker ps -a

# here you could find the container id

docker commit XXXXXXXXX mudongliang/edb-34164

docker login

# login in with your dockerhub account

docker push
```
