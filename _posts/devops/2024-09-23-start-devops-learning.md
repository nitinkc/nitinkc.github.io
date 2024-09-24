---
title:  "DevOps Learning - Starting point"
date:   2024-09-23 20:14:00
categories: [Miscellaneous] 
tags: [Miscellaneous]
---

Start Docker 

Start minikube
```shell
minikube start
```

In a separate terminal tab, start minikube dashboard
```shell
minikube dashboard
```

All Dev Ops projects are at [https://github.com/nitinkc/GitOps](https://github.com/nitinkc/GitOps)


## Microservice 
Make any changes to the [https://github.com/nitinkc/messenger-spring-boot/tree/master](https://github.com/nitinkc/messenger-spring-boot/tree/master)

The circle-ci pipeline is setup to push the latest build image to docker. [Code](https://github.com/nitinkc/messenger-spring-boot/blob/master/.circleci/config.yml)

## Release with flux
On the minikube cluster running on local

Goto [Helm Repo project](https://github.com/nitinkc/HelmCharts/tree/main)

```shell
helm repo update
helm upgrade --install todo-service-app myrepo/todo-app      
```

