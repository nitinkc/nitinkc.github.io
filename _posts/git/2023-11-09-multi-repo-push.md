---
title:  "Git - Multi Repo projects "
date:   2023-11-03 14:30:00
categories: ['Git']
tags: ['Git']
---

Add and update two repositories simultaneously




{% gist nitinkc/81c53424cf60e8742b30df02a844906c %}


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


## Scenario 1

```shell
create a new branch feature/git-squash-commit-test

# Sets the default repo to BitBucket
git push --set-upstream bb feature/git-squash-commit-test

# After some commits 
git push #takes the changes to bb
pit push 
```

# Logs
```log
❯ git push
Enumerating objects: 5, done.                                                                                    ─╯
Counting objects: 100% (5/5), done.
Delta compression using up to 16 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 280 bytes | 280.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/nitinkc/git-tests.git
   86870ce..85d75b5  main -> main
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 16 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 280 bytes | 280.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
To https://bitbucket.org/nitinc/git-tests-bb.git
   86870ce..85d75b5  main -> main
╭─░▒▓    ~/Downloads/git-tests ─
```

`git push <remote-name> <branch-name>`

By default, the branch main is declared with `git init` command als it also sets `remote "origin"` with git re

`git init` creates the following git config
```editorconfig
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
	ignorecase = true
	precomposeunicode = true
```

The following remote add command creates the next config `remote "origin"`
```shell
git remote set-url <remote_name> <remote_url>
# Commands provided from git repo
git remote add origin https://github.com/nitinkc/git-tests.git
```

```editorconfig
[remote "origin"]
	url = https://github.com/nitinkc/git-tests.git
	fetch = +refs/heads/*:refs/remotes/origin/*
```

When there is a new branch created in workspace/local repository, before pushing it to repo, `-u` or `--set-upstream` 
option is used which adds an entry into the git config

```shell
git push -u origin main
```

```editorconfig
[branch "main"]
    remote = origin
    merge = refs/heads/main
```

For each subsequent push to a feature branch,
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

Taking the leveragew of the remote created automatically, we can create multiple **remotes** and push explicitly into those

The full command for the push is
```shell
git push <remote-name> <branch-name>
```

We can create a new remote called **bb** by


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





# Summary

##### Add multiple remote Repo
git remote add bb https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
git remote add gh https://github.com/nitinkc/git-tests.git

##### Apply actions
git remote set-url --push bb https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
git remote set-url --push gh https://github.com/nitinkc/git-tests.git
