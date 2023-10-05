---
title:  "Docker"
date:   2023-10-04 20:01:00
categories: [Microservices]
tags: [Microservices]
---

# Docker commands

```shell
docker ps # shows running containers

docker ps --all # see all the running and exited containers

docker system prune # remove all the exited container

```

### Docker Logs

```shell
docker logs <container_id>
```

### Execute a command inside a container

-i -t flag Allows us to provide input to the container

{: .notice--primary} docker exec -it <container_Id> <command to execute>

```shell
docker run redis

docker ps <id>

docker exec -it 3bd4306ce6b3 redis-cli
```