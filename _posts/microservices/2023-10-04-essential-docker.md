---
title:  "Docker"
date:   2023-10-04 20:01:00
categories: [Microservices]
tags: [Microservices]
toc: true
---

# Docker commands

### Docker containers

```shell
# Start Docker Container
docker start <CONTAINER ID>
# Stop Running Docker Container
docker stop <CONTAINER ID>
# Delete Docker Container
docker rm <CONTAINER ID>
```

### Currently Running Docker Containers

```shell
docker ps # shows running containers
docker ps --all # see all the running and exited containers
```

### Docker Images

```shell
# List Docker Images on Computer
docker images -a

# Remove Docker Image
docker rmi <IMAGE ID>
#or
docker rmi -f <IMAGE ID>

#Remove All Docker Images on Computer
docker rmi $(docker images -f dangling=true)

# remove all the exited container
docker system prune 
```

## Run Docker Image in Docker Container

```shell
# -d switch is for detached process i.e command prompt is back
docker run -d <IMAGE NAME> 
```

### Docker Logs and inspect

```shell
docker logs <container_id>
docker inspect <container_id>

```

### Execute a command inside a container

-i -t flag Allows us to provide input to the container

docker exec -it <container_id> <command to execute>
{: .notice--primary}

```shell
docker run redis # If the image is not there, then it will download

docker ps <id>

docker exec -it 3bd4306ce6b3 redis-cli
# Exit or Quit to come out of the prompt
```

one liner

```shell
docker run -it busybox sh

docker exec -it 67e36143717b ls
```

### Pass Environment Variables


docker run ceaf9e1ebef5 -e "SPRING_PROFILES_ACTIVE=dev" -e "server.port=8080"


### Entering the shell of a container


### Tagging an image

```shell
# Last parameter specifies the directory of files/folders to use for a build
docker build -t nitinkc/redis-server:latest . 

# Run the image from the docker hub
docker run nitinkc/redis-server
```

# Docker build

```shell
docker build -t nitinkc/simpleweb .
docker run -it nitinkc/simpleweb sh

docker run -p 8080:8080 nitinkc/simpleweb
```

## Docker compose
```shell
docker-compose up

docker-compose down
```