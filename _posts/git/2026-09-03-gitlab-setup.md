---
title: GitLab Config
date: 2026-09-03 10:30:00
categories:
- GitLab
tags:
- Configuration
- Settings
- Setup
- Commands
---

## Update brew

```shell
brew update && brew outdated && brew upgrade && brew cleanup && brew autoremove && brew cleanup --prune=all
```

## Install gitlab cli and configure

run one by one
```shell
brew install glab

# Optional :if not already set
git config --global user.name "Your Full Name"
git config --global user.email "your.email@org.com"

# check login via PAT from gitlab
glab auth login --hostname gitlab.gcp.corp.com
```

### Clone all projects under a gitlab directory

```shell
glab config set host gitlab.gcp.davita.com

# cd into the fresh directory where the cloning is needed
glab repo clone \
--group corp-apps/my-project-initiative \
--include-subgroups \
--paginate \
--preserve-namespace \
--archived=false

# OR, temp fix
GITLAB_HOST=gitlab.gcp.corp.com glab repo clone \
  --group corp-apps/my-project-initiative \
  --include-subgroups \
  --paginate \
  --preserve-namespace \
  --archived=false
```

### inside individual repo

Create a Pull request 
```shell
glab mr create
```

## Config tweaking

```shell
glab config path
glab config path --dir

glab config get host
```

change host
```shell
glab config set host gitlab.com
```
