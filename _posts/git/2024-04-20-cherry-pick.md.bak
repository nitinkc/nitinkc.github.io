---
categories: Git
date: 2024-04-20 13:30:00
tags:
- Git
title: Git Cherry Pick
---

Git cherry-pick is a command used to apply a specific commit from one branch to
another.
It's useful when you want to pick only certain commits from one branch and apply
them to another branch, without merging the entire branch

```shell
#Get the commit hash of the commit that needs to be cherry picked or use intelliJ History
git log

#Checkout the branch where cherry pick is needed
git checkout main

git cherry-pick 1dc53a7e
git add README.md
git cherry-pick --continue
git push
```