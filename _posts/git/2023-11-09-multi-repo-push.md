---
title:  "Git config- Multi Repo projects"
date:   2023-11-13 14:30:00
categories: ['Git']
tags: ['Git']
---
{% include toc title="Index" %}

### git init
`git init` creates the following entry in config file in `.git` folder

```dotenv
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
	ignorecase = true
	precomposeunicode = true
```

### 1. remote add
The following `remote add` creates the next config `remote "origin"`
```shell
# Commands provided from git repo
git remote add origin https://github.com/nitinkc/git-tests.git
```

```editorconfig
[remote "origin"]
	url = https://github.com/nitinkc/git-tests.git
	fetch = +refs/heads/*:refs/remotes/origin/*
```

### 2. remote set-url
The remote repo can be **set to another repo** if needed
- if the project already exists. This will **replace** the old remote
```shell
# If the project is already a git project and you want to set github repo to the existing project
git remote set-url <remote_name> <remote_url>
git remote set-url origin https://github.com/nitinkc/x.git
```
- replacing the old repo `git-tests.git` with the new one `x.git`

```editorconfig
[remote "origin"]
	url = https://github.com/nitinkc/x.git
	fetch = +refs/heads/*:refs/remotes/origin/*
```

##### 3. The `push` switch
```shell
git remote set-url --push origin https://github.com/nitinkc/git-tests.git
```

This sets up the push url

```editorconfig
[remote "origin"]
	url = https://github.com/nitinkc/git-tests.git
	fetch = +refs/heads/*:refs/remotes/origin/*
	pushurl = https://github.com/nitinkc/git-tests.git
```


# git push
The full command for the push is
```shell
git push <remote-name> <branch-name>
```

If you set up tracking for your **existing** branch using
```shell
git branch --set-upstream-to=<remote>/<remote-branch> <local-branch>
```

Or set up a new branch with `-u` or `--set-upstream`
```shell
git push -u <remote-name> your-new-branch
git push --set-upstream origin feature/intermittant-failures
```

then the simple command will do the job
```shell
git push
```

When there is main branch created, after git init, for the first time, in workspace/local repository, before pushing it to repo, `-u` or `--set-upstream` 
option is used which adds an entry into the git config

```shell
git push -u origin main
# OR
git push --set-upstream origin main
```

```editorconfig
[branch "main"]
    remote = origin
    merge = refs/heads/main
```

For each subsequent push to a new feature branch,
```shell
git checkout -b feature/new-feature-branch

git push # fatal: The current branch feature/new-feature-branch has no upstream branch.
git push --set-upstream origin feature/new-feature-branch
```
git config gets one entry
```editorconfig
[branch "feature/new-feature-branch"]
	remote = origin
	merge = refs/heads/feature/new-feature-branch
```

# git pull
The git pull command is used to fetch & merge changes from a **remote** repository into the current branch
```shell
git pull [<remote>] [<branch>]
git pull both main
```
notice that both remote and branch names are optional. When there is tracking from that particular branch,
a simple `git pull` will do the job.


# Multi Repo setup
Taking the leverage of the remote created automatically, we can create multiple **remotes** and push explicitly into those

We can create a new remote called **bb** by
```shell
git remote add bb https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
```

Following entry gets made in gitconfig
```editorconfig
[remote "bb"]
    url = https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
    fetch = +refs/heads/*:refs/remotes/bb/*
```

Also, set the push url with
```shell
git remote set-url --push gh https://github.com/nitinkc/git-tests.git
```

This will modify the gitconfig as below :-
```editorconfig
[remote "bb"]
	url = https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
	fetch = +refs/heads/*:refs/remotes/bb/*
	pushurl = https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
```

### create for both

```shell
# Add the remote with fetch URL
git remote add both https://github.com/nitinkc/git-tests.git

# Add an additional URL for push
git remote set-url --add --push both https://github.com/nitinkc/git-tests.git
git remote set-url --add --push both https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
```

Adds two repositories into remote `both` and sets them up for simultaneous pushes and pulls.
```editorconfig
[remote "both"]
	url = https://github.com/nitinkc/git-tests.git
	fetch = +refs/heads/*:refs/remotes/both/*
	pushurl = https://github.com/nitinkc/git-tests.git
	pushurl = https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
```


```shell
git branch --set-upstream-to=both/feature/new-feature-branch feature/new-feature-branch 
```
```editorconfig
[branch "feature/new-feature-branch"]
remote = both
merge = refs/heads/feature/new-feature-branch
```

## The final gitconfig file
{% gist nitinkc/81c53424cf60e8742b30df02a844906c %}


if `git push both` is issued on the repo

```shell
Everything up-to-date
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
remote: 
remote: Create pull request for feature/new-feature-branch:
remote:   https://bitbucket.org/nitinc/git-tests-bb/pull-requests/new?source=feature/new-feature-branch&t=1
remote: 
To https://bitbucket.org/nitinc/git-tests-bb.git
 * [new branch]      feature/new-feature-branch -> feature/new-feature-branch
```

# Summary

##### Add multiple remote Repo
```shell
git remote add bb https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
git remote add gh https://github.com/nitinkc/git-tests.git
```

##### Apply actions
```shell
git remote set-url --push bb https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
git remote set-url --push gh https://github.com/nitinkc/git-tests.git
```

##### Push & Pull

Usual work with two repositories simultaneously

```shell
# create a new branch feature/git-squash-commit-test
git checkout -b feature/git-squash-commit-test

# Sets the default repo to BitBucket
git push --set-upstream bb feature/git-squash-commit-test
git branch --set-upstream-to=both/feature/new-feature-branch feature/new-feature-branch 

# After some commits 
git push #takes the changes to bb
```


```shell
git pull gh
git pull bb

git fetch gh
git fetch bb

git merge origin/main
git merge bb/main
git merge gh/main

git push bb main
git push gh main
```
