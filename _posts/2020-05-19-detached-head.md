---
title:  "Detached Head Problem"
date:   2020-05-19 19:14:00
categories: Git
tags: [Git, submodules]
---

While using Git Submodules, after cloning a submodule, the projects are in detached
mode.

[Use this link for the resolution](https://github.com/nitinkc/git-submodule-demo/blob/master/README.md)

```sh
git log --graph --decorate --pretty=oneline --abbrev-commit master origin/master
git log -n 2
git checkout 957833d728b3249d22a3b3160f3a48b72c576d91
git checkout -b temp
git checkout master
git merge temp
// delete branch locally
git branch -d temp
```
