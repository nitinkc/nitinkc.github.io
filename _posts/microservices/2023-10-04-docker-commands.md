---
title:  "Docker commands"
date:   2023-10-04 20:01:00
categories: [Microservices]
tags: [Microservices]
---

{% include toc title="Index" %}

# Docker container

Running an image that exist on local machine 

### Start existing

```shell
# Start Docker Container
docker start <CONTAINER ID>
# Stop Running Docker Container
docker stop <CONTAINER ID>
# Delete Docker Container
docker rm <CONTAINER ID>
```

### Start new 

Run Docker Image in Docker Container

```shell
# -d switch is for detached process i.e command prompt is back
docker run -d <IMAGE NAME> 
```

### Check Running Containers

```shell
docker ps # shows running containers
docker ps --all # see all the running and exited containers
# List all containers, both running and stopped
sudo docker ps -a
sudo docker ps -aq #quiet

docker ps -l

# Cleaning

# Remove Containers
docker container rm 6d0806087e50
docker container rm 8cf7ae980534

docker system prune
```

### Docker Logs and inspect

```shell
docker logs <container_id>
docker inspect <container_id>
```

### Enter the Shell

Execute a command inside the shell of a container

`-i -t` flag Allows us to provide input to the container

docker exec -it <container_id> <shell-executable>
{: .notice--primary}

```shell
docker run --name redis-local redis # If the image is not there, then it will download
docker ps <id>

docker exec -it redis-local redis-cli
# Exit or Quit to come out of the prompt
```

one liner

```shell
# Start and run the shell inside busybox
docker run -it --name my-busybox busybox sh

# Start and existing container
docker start my-busybox #<busybox_id>

# Just execute the command and back to command prompt 
docker exec -it my-busybox ls
```

### Pass Environment Variables

```shell
docker run ceaf9e1ebef5 -e "SPRING_PROFILES_ACTIVE=dev" -e "server.port=8080"

docker run -d \
    --name=mysql_learning \
    --env="MYSQL_ROOT_PASSWORD=root" \
    --env="MYSQL_PASSWORD=root" \
    -v ~/Downloads/docker_data:/var/lib/mysql \
    -p=3306:3306 \
    mysql

docker exec -it mysql_learning mysql -uroot -proot

```

# Docker Images

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


# Docker build

### Tagging an image

* the build command takes image name
* the run command takes container name


```shell
# Last parameter specifies the directory of files/folders to use for a build
docker build -t nitinkc/my-spring-boot-app:latest . 
docker build -t my-spring-boot-app . #Without repo name

# Run the image from the docker hub
docker run -p 8080:8080 nitinkc/simpleweb
```

# Publish Docker Image to Docker Hub

### Summary (Docker hub images)

1. Create Repository on https://hub.docker.com/ . <repo-name>
2. Log into the Docker Hub from the command line
`docker login --username=xxxxx --email=xxxxx` or simply `docker login`
2. Check the image ID (on local machine)using `docker images`
3. Tag the image `docker tag <image-name> dockerhub-user-name/<repo-name>:tag-name`
4. Push the image to the repository  created `docker push dockerhub-user-name/<repo-name>`


```shell
# Build the image using the Dockerfile in the project
docker build . --file Dockerfile --tag test-image

# Check the image created after the build
docker image ls

# Docker image
docker login

# Tag the image if not done while build
docker tag <CONTAINER ID> <DOCKER USERNAME>/<REPO>
docker tag test-image nitinkc/test-image

# Push the image
docker push nitinkc/test-image
# long form of the same command
docker image push nitinkc/test-image 
```

# Directory Binding 

Bind a Directory in Docker Container to a Directory on Host Machine

The -v switch is used

-v <directory on HOST machine>:<directory in Docker container>
{: .notice--primary}

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

Spring boot on Docker container running on port 5000, mapped with port 8080 of the local machine.
```shell
docker run --publish 8080:5000 -t nitinkc/todo-app:todo-backend-26

docker run -p 8080:5000 nitinkc/todo-app:todo-backend-26
```

```shell
docker run nitinkc/todo-app:todo-backend-26 --network host
```

# Docker compose

[Sample project for Docker Compose to build a Postgres DB and initialize with sample data](https://github.com/nitinkc/DockerConcepts/tree/master/docker-compose)

```shell
docker-compose up

docker-compose down
```

# Dockerfile

```dockerfile
#one CMD command (the last one always) executed per `Dockerfile`
# Use an existing docker image as a base
FROM openjdk:11

# Take the file from host machine into the container
# the dot (.) current directory w.r.t Dockerfile is located
# `/usr/src/myapp` : destination path inside the Docker image
COPY ./java_files /usr/src/myapp

# the absolute path set the working directory
WORKDIR /usr/src/myapp

RUN javac *.java

CMD ["java", "Main"]
```

# Multistage Docker build

For a gradle project, where the build is done in stage 1 and is used in stage 2

```dockerfile
#Build stage
FROM gradle:latest AS BUILD
WORKDIR /usr/app/
COPY . .
RUN gradle clean build

# Package stage
FROM openjdk:latest
ENV JAR_NAME=java-docker-experiments-1.0.jar
ENV APP_HOME=/usr/app/
WORKDIR $APP_HOME
COPY --from=BUILD $APP_HOME .
ENTRYPOINT exec java -jar $APP_HOME/build/libs/$JAR_NAME
```

# Automate Docker push

The Automation can be done via circle-ci, github-work flow or any other automation engines

### Gradle Project

The docker file takes care of compiling and generating the jar file
[Multistage Docker file](https://github.com/nitinkc/docker-multistage-gradle/blob/main/Dockerfile)

Check the version numebr increment in the git workflow `docker-publish.yml` file
[Example of Github workflow](https://github.com/nitinkc/docker-multistage-gradle/blob/main/.github/workflows/docker-publish.yml)

### Maven Project

[Maven Project](https://github.com/nitinkc/messenger-spring-boot/tree/master) with [docker file](https://github.com/nitinkc/messenger-spring-boot/blob/master/Dockerfile)

[Example of Circle-ci](https://github.com/nitinkc/messenger-spring-boot/blob/master/.circleci/config.yml)

[Circle-CI pipeline](https://app.circleci.com/pipelines/github/nitinkc/messenger-spring-boot)

{% gist nitinkc/369ffd7a41871c1fbc335529fb6be9e0 %}


##### Simpler Version

{% gist nitinkc/7965906df336c8d19ff5315e0f1f0549 %}


# Docker compose with SpringBoot

**Project Readme**

[https://github.com/nitinkc/DockerConcepts/tree/master/6-dockerCompose-springboot-redis/visits#readme](https://github.com/nitinkc/DockerConcepts/tree/master/6-dockerCompose-springboot-redis/visits#readme)

The `docker-compose` file which uses the Dockerfile to build and execute the `Dockerfile`

[https://github.com/nitinkc/DockerConcepts/blob/master/6-dockerCompose-springboot-redis/visits/docker-compose.yaml](https://github.com/nitinkc/DockerConcepts/blob/master/6-dockerCompose-springboot-redis/visits/docker-compose.yaml)

[https://github.com/nitinkc/DockerConcepts/blob/master/6-dockerCompose-springboot-redis/visits/Dockerfile](https://github.com/nitinkc/DockerConcepts/blob/master/6-dockerCompose-springboot-redis/visits/Dockerfile)