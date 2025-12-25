---
categories: Git
date: 2020-05-19 19:14:00
tags:
- Troubleshooting
- Version Control
title: Submodules & Detached Head Problem
---

{% include toc title="Index" %}

# Add a new project in an existing submodule
```shell
git submodule add <GitHub Repo Name>
```

# Initialize new submodule
```shell
git submodule init
git submodule update 
```

# Clone all projects in submodule
Fetch up to 6 submodules at a time (in parallel) with `-j6`

```shell
git clone --recurse-submodules -j6 https://github.com/nitinkc/spring-microservices.git

git clone --recurse-submodules -j8 https://github.com/nitinkc/SpringBootProjects.git
```

In case `git clone` is used on a submodule parent project
```shell
git clone https://github.com/nitinkc/spring-microservices.git
cd spring-microservices
## Update all the submodules
git pull --recurse-submodules
```

** For Submodules to be tracked using a branch instead of a commit **.
Add the branch name in the `.gitmodules` file
```shell
[submodule "foo"]
    path = foo
    url = ...
    branch = main
```

This will check out the tip of the branch (e.g., main) in the submodule, instead of a fixed commit.
```sh
git submodule update --remote
```

# In case the projects needs be deleted

```shell
git submodule deinit -f -- my-project #provide the project to be removed
git rm --cached my-project                                        
```

* Delete the entry from `.gitmodules` file
* Commit and push the changes on github

Cleaning the local `.git` repo.

* delete the entry from `.git/config` file
* delete the project folder from `.git/modules/<git-project-name>`

> Instead of this, just commit the `.gitmodules` changes and re-clone the project

# Detached Head Problem
While using Git Submodules, after cloning a submodule, the projects are in detached mode.

### [Use this link for the resolution](https://github.com/nitinkc/git-submodule-demo/blob/master/README.md)

```sh
git log --graph --decorate --pretty=oneline --abbrev-commit master origin/master
git log -n 2
git checkout 957833d728b3249d22a3b3160f3a48b72c576d91
git checkout -b temp
git checkout master
git merge temp
# delete branch locally
git branch -d temp
```