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

```shell
docker run ceaf9e1ebef5 -e "SPRING_PROFILES_ACTIVE=dev" -e "server.port=8080"

docker run -d \
    --name=mysql_learning \
    --env="MYSQL_ROOT_PASSWORD=root" \
    --env="MYSQL_PASSWORD=root" \
    -v ~/Downloads/docker_data:/var/lib/mysql \
    -p=3306:3306 mysql

docker exec -it mysql_learning mysql -uroot -proot

```

### Entering the shell of a container


# Docker build

### Tagging an image

```shell
# Last parameter specifies the directory of files/folders to use for a build
docker build -t nitinkc/my-spring-boot-app:latest . 
docker build -t my-spring-boot-app .

# Run the image from the docker hub
docker run nitinkc/redis-server
```

```shell
docker build -t nitinkc/simpleweb .
docker run -it nitinkc/simpleweb sh

docker run -p 8080:8080 nitinkc/simpleweb
```

# Publish Docker Image to Docker Hub

```shell
# Build the image using the Dockerfile in the project
docker build . --file Dockerfile --tag test-image

# Check the image created after the build
docker image ls

# Docker image
docker login

# Tag the image
docker tag <CONTAINER ID> <DOCKER USERNAME>/<REPO>
docker tag test-image nitinkc/test-image

# Push the image
docker push <Docker Hub User name>/<Repository name>
docker push nitinkc/test-image
# long form of the same command
docker image push nitinkc/test-image 
```

# Bind a Directory in Docker Container to a Directory on Host Machine

The -v switch is used

> -v <directory on HOST machine>:<directory in Docker container>

```shell
docker run -d \
    --name=mysql_learning \
    --env="MYSQL_ROOT_PASSWORD=root" \
    --env="MYSQL_PASSWORD=root" \
    -v ~/Downloads/docker_data:/var/lib/mysql \
    -p=3306:3306 mysql
```

# Docker Networks on Local Computer

```shell
docker network ls
#Create Custom Docker Bridge Network
docker network create --driver bridge <NETWORK NAME>
```
Run Docker container in the newly created custom bridge network

```shell
docker run <CONTAINER ID > --network <NAME OF CREATED NETWORK>
```

### Avoid Port Binding

Make Docker Container use Host Network to Avoid Port Binding

> docker run <IMAGE ID> --network host

```shell
docker run --publish 8080:5000 -t nitinkc/todo-app:todo-backend-26

docker run -p 8080:5000 nitinkc/todo-app:todo-backend-26
```

Spring boot on Docker container running on port 5000, mapped with port 8080 of the local machine.


```shell
docker run nitinkc/todo-app:todo-backend-26 --network host
```

## Docker compose

[Sample project for Docker Compose to build a Postgres DB and initialize with sample data](https://github.com/nitinkc/DockerConcepts/tree/master/docker-compose)

```shell
docker-compose up

docker-compose down
```